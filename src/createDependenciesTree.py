import subprocess
import shutil
import json
from os.path import join
from os import getcwd
from subprocess import PIPE, STDOUT
from activate_virtualenv import activate_virtualenv
from retrieveLocallyLicensesInformation import ReceiveLocallyLicensesInformation
from pypi_lcv_logging import logger


class DependenciesTree:
    @staticmethod
    def create_dependencies_tree(requirements_txt: str, project_name: str):
        """
        Create a virtualenv and activate it. Then it installs and runs pipdeptree to create
        the dependencies tree. It saves pipdeptree output as a json file and return its path.

             Args:
                 requirements_txt (str): the path containing the Requirements.txt of the analyzed project
                 project_name (str): the project name set as a command line parameter.
        """
        venv_dir = join(getcwd(), f'venv-{project_name}')
        result = subprocess.run(['python3', '-m', 'venv', f'venv-{project_name}'],  stdout=PIPE, stderr=STDOUT)
        logger.info(f'python3 -m venv venv-{project_name}')
        logger.info(result.stdout)
        try:
            shutil.copyfile('./activate_this.py', f'{venv_dir}/bin/activate_this.py')
        except IOError as e:
            logger.info("Unable to copy file. %s" % e)
        pip3_venv = f'{venv_dir}/bin/pip3'
        with activate_virtualenv(venv_dir):  # run pip install and pipdeptree inside the virtualenv
            result = subprocess.run([pip3_venv, "install", "-r", join(getcwd(), requirements_txt)], cwd=venv_dir,
                                    stdout=PIPE, stderr=STDOUT)
            logger.info(f'pip3 install -r {join(getcwd(), requirements_txt)}')
            logger.info(result.stdout)
            subprocess.run([pip3_venv, "install", 'pipdeptree'], cwd=venv_dir, stdout=PIPE, stderr=STDOUT)
            dependencies_tree_json_path = join(getcwd(), project_name)
            dep_tree_json_file = open(f"{dependencies_tree_json_path}/dependencies_tree.json", "w")
            result = subprocess.run(['pipdeptree', '--json-tree'], cwd=venv_dir,
                                    stdout=dep_tree_json_file, stderr=STDOUT)
            logger.info(f'pipdeptree --json-tree')
            logger.info(result.stderr)
        result = subprocess.run(['rm', '-rf', venv_dir], stdout=PIPE, stderr=STDOUT)  # delete the created venv
        logger.info(f'rm -rf {venv_dir}')
        logger.info(result.stdout)
        return dep_tree_json_file

    @staticmethod
    def increase_dependency_tree_with_license_information(dependencies_tree_path: str):
        """
        It parses the pipdeptree json file augmenting it with license information.
        It returns a json augmented with license information.

            Args:
             dependencies_tree_path (str): the path containing the pipdeptree json file
        """
        with open(dependencies_tree_path, "r") as jsonFile:
            dep_tree = json.load(jsonFile)
        for dependency in dep_tree:
            DependenciesTree.increase_dependencies_with_licenses(dependency)
        dependencies_tree_path = dependencies_tree_path.replace('.json', '')
        with open(f'{dependencies_tree_path}_with_licenses.json', "w") as jsonFile:
            json.dump(dep_tree, jsonFile, indent=4)
        return f'{dependencies_tree_path}_with_licenses.json'

    @staticmethod
    def increase_dependencies_with_licenses(dependency: dict):
        """
        Recursively augment dependencies with license information.

            Args:
             dependency (dict): a dict containing dependency information
        """
        logger.info(dependency['package_name'])
        PyPILicense, PyPILicenseSPDX, GitHubLicense, GitHubLicenseSPDX \
            = (ReceiveLocallyLicensesInformation.
                receive_locally_licenses_information_single_package(
                    dependency['package_name'], dependency['installed_version']))
        dependency['PyPILicense'] = PyPILicense
        dependency['PyPILicenseSPDX'] = PyPILicenseSPDX
        dependency['GitHubLicense'] = GitHubLicense
        dependency['GitHubLicenseSPDX'] = GitHubLicenseSPDX
        dependency['dependencies'] = dependency.pop('dependencies')
        if len(dependency['dependencies']) > 0:
            for dependency in dependency['dependencies']:
                DependenciesTree.increase_dependencies_with_licenses(dependency)

    @staticmethod
    def analyze_dep_tree_with_license_info_recursive(dependencies_tree_with_license_path: str):
        with open(dependencies_tree_with_license_path, "r") as jsonFile:
            data = json.load(jsonFile)
            for dependency in data:
                DependenciesTree.recurse_over_dependency(dependency)

    @staticmethod
    def recurse_over_dependency(dict_obj: dict):
        outbound_license = None
        inbound_licenses_list = []
        inbound_and_outbound_data = {'inbound': {}}
        for key, value in dict_obj.items():
            if 'dependencies' in key:
                for item in value:  # loop over the dependencies
                    DependenciesTree.recurse_over_dependency(item)
                    license_set, source = DependenciesTree.set_license(item)
                    inbound_licenses_list.append(license_set)
                    inbound_and_outbound_data['inbound'][item['package_name']] = \
                        {"package_name": item['package_name'],
                         "SPDX_license": license_set, "license_origin": source}
            if 'package_name' in key:
                outbound_license, source = DependenciesTree.set_license(dict_obj)
                inbound_and_outbound_data['outbound'] = \
                    {"package_name": dict_obj['package_name'],
                     "SPDX_license": outbound_license, "license_origin": source}
                continue

            if len(inbound_licenses_list) > 0 and outbound_license is not None:
                logger.info(f'In this iteration: inbound licenses: {inbound_licenses_list} - '
                            f'and outbound license: {outbound_license} - found')

                logger.info(inbound_and_outbound_data)

    @staticmethod
    def set_license(item: dict):
        license_set = ""
        source = ""
        if item['PyPILicenseSPDX'] is not None and item['PyPILicenseSPDX'] != "":
            license_set = item['PyPILicenseSPDX']
            source = 'PyPI API'
            logger.info(f'Package: {item["package_name"]} - PyPI license: {item["PyPILicenseSPDX"]}')
        else:
            if item['GitHubLicenseSPDX'] is not None and item['GitHubLicenseSPDX'] != "":
                license_set = item['GitHubLicenseSPDX']
                source = 'GitHub API'
                logger.info(f'Package: {item["package_name"]} - GitHub license: {item["GitHubLicenseSPDX"]}')
        return license_set, source
