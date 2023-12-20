import subprocess
import shutil
import json
from os.path import join
from os import getcwd
from subprocess import run
from activate_virtualenv import activate_virtualenv
from retrieveLocallyLicensesInformation import ReceiveLocallyLicensesInformation


class DependenciesTree:
    @staticmethod
    def create_dependencies_tree(requirements_txt, project_name):
        venv_dir = join(getcwd(), f'venv-{project_name}')
        subprocess.run(['python3', '-m', 'venv', f'venv-{project_name}'])
        shutil.copyfile('./activate_this.py', f'{venv_dir}/bin/activate_this.py')
        pip3_venv = f'{venv_dir}/bin/pip3'
        with activate_virtualenv(venv_dir):  # run pip install and pipdeptree inside the virtualenv
            run([pip3_venv, "install", "-r", join(getcwd(), requirements_txt)], cwd=venv_dir)
            run([pip3_venv, "install", 'pipdeptree'], cwd=venv_dir)
            dependencies_tree_json_path = join(getcwd(), project_name)
            f = open(f"{dependencies_tree_json_path}/dependencies_tree.json", "w")
            subprocess.run(['pipdeptree', '--json-tree'], cwd=venv_dir, stdout=f)
            print(type(f))
        return f

    @staticmethod
    def increase_dependency_tree_with_license_information(dependencies_tree_path):
        with open(dependencies_tree_path, "r") as jsonFile:
            dep_tree = json.load(jsonFile)
        for dependency in dep_tree:
            DependenciesTree.collect_dependency_license(dependency)
            if len(dependency['dependencies']) > 0:
                for dependency in dependency['dependencies']:
                    DependenciesTree.collect_dependency_license(dependency)
                    if len(dependency['dependencies']) > 0:
                        for dependency in dependency['dependencies']:
                            DependenciesTree.collect_dependency_license(dependency)
                            if len(dependency['dependencies']) > 0:
                                for dependency in dependency['dependencies']:
                                    DependenciesTree.collect_dependency_license(dependency)
        dependencies_tree_path = dependencies_tree_path.replace('.json', '')
        with open(f'{dependencies_tree_path}_with_licenses.json', "w") as jsonFile:
            json.dump(dep_tree, jsonFile, indent=4)
        return

    @staticmethod
    def collect_dependency_license(dependency):
        print(dependency['package_name'])
        PyPILicense, PyPILicenseSPDX, GitHubLicense, GitHubLicenseSPDX \
            = (ReceiveLocallyLicensesInformation.
                receive_locally_licenses_information_single_package(
                    dependency['package_name'], dependency['installed_version']))
        dependency['PyPILicense'] = PyPILicense
        dependency['PyPILicenseSPDX'] = PyPILicenseSPDX
        dependency['GitHubLicense'] = GitHubLicense
        dependency['GitHubLicenseSPDX'] = GitHubLicenseSPDX
        dependency['dependencies'] = dependency.pop('dependencies')
        return
