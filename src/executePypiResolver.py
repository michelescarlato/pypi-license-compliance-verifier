import pypiResolver

'''
* SPDX-FileCopyrightText: 2023 Michele Scarlato
*
* SPDX-License-Identifier: Apache-2.0
'''


class ExecutePypiResolver:

    @staticmethod
    def execute_pypi_resolver(requirements_txt, package_list):
        print("Resolve dependencies...")
        resolved_packages = pypiResolver.run_pip(requirements_txt, True)

        # packages who break the call graph generation
        broken_list = ["pytest", "future", "python-heatclient", "PyYAML", "rcssmin", "Click",
                       "py", "openstacksdk", "Django", "pyScss", "python-neutronclient", "Pygments",
                       "Pint", "cryptography", "django_openstack_auth", "setuptools", "pyinotify",
                       "rjsmin", "tqdm", "fonttools", "pycodestyle", "pyrsistent", "Dj", "Pt"]

        for package in resolved_packages[1]:
            if package[0] not in broken_list:
                dct = {"name": package[0],
                       "version": package[1],
                       "cg_file": None,
                       "vulnerabilities": None,
                       "callables": None}
                package_list.append(dct)
            else:
                print(f'{package[0]} not inserted because pypi skipped from  ')
        for package in package_list:
            for broken in broken_list:
                if broken == package["name"]:
                    package_list.remove(package)
        print("Dependencies resolved.")
        return package_list

    @staticmethod
    def execute_pypi_resolver_for_licensing(requirements_txt):
        package_list = []
        print("Resolve dependencies...")
        resolved_packages = pypiResolver.run_pip(requirements_txt, True)
        for package in resolved_packages[1]:
            dct = {"name": package[0],
                   "version": package[1],
                   "cg_file": None,
                   "vulnerabilities": None,
                   "callables": None}
            package_list.append(dct)
        print("Dependencies resolved.")
        return package_list
