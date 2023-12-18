import json
import requests
import time
from urllib.parse import urlparse
from lcvlib.SPDXIdMapping import ConvertToSPDX, IsAnSPDX

'''
* SPDX-FileCopyrightText: 2022 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: Apache-2.0
'''


def retrieve_github_url(json_response, package_name):
    global url
    url = ""
    response = json.dumps(json_response)
    data = json.loads(response)
    if data['info']['home_page'] is not None:
        if package_name in data['info']['home_page']:
            if "https://github.com/" in data['info']['home_page']:
                url = data['info']['home_page']
                return url
    if data['info']['project_urls'] is not None:
        if 'Homepage' in data['info']['project_urls']:
            if package_name in data['info']['project_urls']['Homepage']:
                if "https://github.com/" in data['info']['project_urls']['Homepage']:
                    url = data['info']['home_page']
                    return url
    iterdict(data, package_name)
    return url


def iterdict(d, package_name):
    global url
    for k, v in d.items():
        if k != "description":
            if isinstance(v, dict):
                iterdict(v, package_name)
            else:
                if "https://github.com/" in str(v):
                    if package_name in str(v):
                        url = str(v)
                        return url


def retrieve_github_api_url(github_url):
    parts = urlparse(github_url)
    directories = parts.path.strip('/').split('/')
    owner = directories[0]
    repo = directories[1]
    github_url = "https://api.github.com/repos/" + owner + "/" + repo + "/license"
    return github_url


def retrieve_license_from_github(github_api_url, lcv_url):
    GitHubLicense = ""
    GitHubLicenseSPDX = ""
    try:
        response = requests.get(url=github_api_url)  # get Call Graph for specified package
        if response.status_code == 200:
            jsonResponse = response.json()  # save Call Graph as JSON format
            GitHubLicense = (jsonResponse["license"]["spdx_id"])
            if len(GitHubLicense) == 0:
                GitHubLicense = (jsonResponse["license"]["key"])
            if len(GitHubLicense) == 0:
                GitHubLicense = (jsonResponse["license"]["name"])
            # here a call to the LCV endpoint convertToSPDX endpoint should be performed
            if len(GitHubLicense) > 0:
                # check if the retrieved license is an SPDX id
                IsSPDX = is_an_spdx(GitHubLicense, lcv_url)
                if not IsSPDX:
                    SPDXConversion = convert_to_spdx(GitHubLicense, lcv_url)
                    IsSPDX = is_an_spdx(SPDXConversion, lcv_url)
                    if IsSPDX:
                        GitHubLicenseSPDX = SPDXConversion
                else:
                    GitHubLicenseSPDX = GitHubLicense
    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)

    return GitHubLicense, GitHubLicenseSPDX


def is_an_spdx(license_name, lcv_url):
    LCVIsAnSPDXJsonResponse = None
    LCVIsAnSPDXurl = f'{lcv_url}IsAnSPDX?SPDXid={license_name}'
    try:
        response = requests.get(url=LCVIsAnSPDXurl)  # get Call Graph for specified package
        if response.status_code == 200:
            LCVIsAnSPDXJsonResponse = response.json()
        if response.status_code == 414:
            LCVIsAnSPDXJsonResponse = False
    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)
    return LCVIsAnSPDXJsonResponse


def convert_to_spdx(license_name, lcv_url):
    LCVConvertToSPDXurl = f'{lcv_url}ConvertToSPDX?VerboseLicense={license_name}'
    try:
        response = requests.get(url=LCVConvertToSPDXurl)  # get Call Graph for specified package
        if response.status_code == 200:
            LCVConvertToSPDXJsonResponse = response.json()
        if response.status_code == 414:
            LCVConvertToSPDXJsonResponse = "Too long license name"
    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)
    return LCVConvertToSPDXJsonResponse


def retrieve_license_information_from_pypi(package_name, package_version, lcv_url):
    URL = f'https://pypi.org/pypi/{package_name}/{package_version}/json'
    PyPILicenseSPDX = ""
    try:
        response = requests.get(url=URL)
        if response.status_code == 200:
            jsonResponse = response.json()
            PyPILicense = (jsonResponse["info"]["license"])
            if PyPILicense is not None:
                if len(PyPILicense) > 0:
                    if not IsAnSPDX(PyPILicense): #, lcv_url):
                        # SPDXConversion = convert_to_spdx(PyPILicense, lcv_url)
                        SPDXConversion = ConvertToSPDX(PyPILicense)
                        if IsAnSPDX(SPDXConversion): #, lcv_url):
                            PyPILicenseSPDX = SPDXConversion
                    else:
                        PyPILicenseSPDX = PyPILicense
    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)
    return PyPILicenseSPDX, PyPILicenseSPDX, jsonResponse



