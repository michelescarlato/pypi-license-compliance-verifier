from gitHubAndPyPIParsingUtils import *

'''
* SPDX-FileCopyrightText: 2022 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: Apache-2.0
'''


class ReceiveLocallyLicensesInformation:
    @staticmethod
    # add the source (e.g. GitHub or PyPI) to the dict!
    def receive_locally_licenses_information(package_list, i):
        licenses = {}
        for package in package_list:
            print(f"package name:{package['name']} package version:{package['version']}")
            if package['name'] is not None and package['version'] is not None:
                licenses[i] = {}
                licenses[i]['packageName'] = package['name']
                licenses[i]['packageVersion'] = package['version']
                PyPILicense, PyPILicenseSPDX, jsonResponse = (
                    retrieve_license_information_from_pypi(package['name'], package['version']))
                if PyPILicense is not None and len(PyPILicense) > 0:
                    licenses[i]['PyPILicense'] = PyPILicense
                if PyPILicenseSPDX is not None and len(PyPILicenseSPDX) > 0:
                    licenses[i]['PyPILicenseSPDX'] = PyPILicenseSPDX
                GitHubURL = retrieve_github_url(jsonResponse, package['name'])
                if GitHubURL is not None and len(GitHubURL) > 0:
                    GitHubAPIurl = retrieve_github_api_url(GitHubURL)
                    if len(GitHubAPIurl) > 0:
                        GitHubLicense, GitHubLicenseSPDX = retrieve_license_from_github(GitHubAPIurl)
                        if GitHubLicense != "":
                            if GitHubLicense is not None:
                                licenses[i]['GitHubLicense'] = GitHubLicense
                        if GitHubLicenseSPDX != "":
                            if GitHubLicenseSPDX is not None:
                                licenses[i]['GitHubLicenseSPDX'] = GitHubLicenseSPDX
                i += 1
        return licenses
    @staticmethod
    def receive_locally_licenses_information_single_package(package_name, package_version):
        GitHubLicense = None
        GitHubLicenseSPDX = None
        PyPILicense, PyPILicenseSPDX, jsonResponse = (
            retrieve_license_information_from_pypi(package_name, package_version))
        GitHubURL = retrieve_github_url(jsonResponse, package_name)
        if GitHubURL is not None and len(GitHubURL) > 0:
            GitHubAPIurl = retrieve_github_api_url(GitHubURL)
            if len(GitHubAPIurl) > 0:
                GitHubLicense, GitHubLicenseSPDX = retrieve_license_from_github(GitHubAPIurl)
        return PyPILicense, PyPILicenseSPDX, GitHubLicense, GitHubLicenseSPDX
