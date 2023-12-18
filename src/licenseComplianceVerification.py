import time
import requests
from lcvlib.verify import Compare_OSADL
'''
* SPDX-FileCopyrightText: 2023 Michele Scarlato
*
* SPDX-License-Identifier: Apache-2.0
'''


def license_compliance_verification(inbound_licenses, outbound_license, lcv_url):
    InboundLicensesString = ';'.join([str(item) for item in inbound_licenses])
    # LCVComplianceAssessment = LCVurl + "LicensesInput?InboundLicenses=" + InboundLicensesString + "&OutboundLicense=" + outbound_license
    #LCVComplianceAssessment = (f'{lcv_url}LicensesInput?InboundLicenses={InboundLicensesString}'
     #                          f'&OutboundLicense={outbound_license}')
    LCVComplianceAssessment = Compare_OSADL(inbound_licenses, outbound_license)
    '''
    try:
        response = requests.get(url=LCVComplianceAssessment)
        if response.status_code == 200:
            LCVComplianceAssessmentResponse = response.json()

    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)
    '''
    return LCVComplianceAssessment


def generate_inbound_license_set(licenses):
    InboundLicenses = []
    for i in licenses:
        PyPILicenseSPDX = licenses[i].get("PyPILicenseSPDX")
        if PyPILicenseSPDX is not None:
            InboundLicenses.append(PyPILicenseSPDX)
        else:
            GitHubLicenseSPDX = licenses[i].get("GitHubLicense")
            if GitHubLicenseSPDX is not None:
                InboundLicenses.append(GitHubLicenseSPDX)
    # removing duplicates from the list
    InboundLicenses = list(dict.fromkeys(InboundLicenses))
    return InboundLicenses


def parse_lcv_assessment_response(lcv_assessment_response_list, licenses):
    assessment = {}
    j = 0  # assessment index
    for lcv_answer in lcv_assessment_response_list:
        if (lcv_answer.get("status")) == "not compatible":
            assessment[j] = {}
            InboundNotCompatibleLicense = (lcv_answer.get("inbound_SPDX"))
            outputNotCompatibleInboundLicense = (lcv_answer.get("message"))
            for i in licenses:
                packageName = licenses[i].get("packageName")
                packageVersion = licenses[i].get("packageVersion")
                if licenses[i].get("PyPILicenseSPDX") == InboundNotCompatibleLicense:
                    # outputPackageInformationNotCompatibleInboundLicensePyPI = "License " + InboundNotCompatibleLicense + \
                    #    ", declared in PyPI, found in " + packageName + " v. " + packageVersion + "."
                    outputPackageInformationNotCompatibleInboundLicensePyPI = (
                            f'License {InboundNotCompatibleLicense}, declared in PyPI, found in {packageName} '
                            f'v. {packageVersion}.')
                    assessment[j]["packageInformation"] = outputPackageInformationNotCompatibleInboundLicensePyPI
                if licenses[i].get("GitHubLicense") == InboundNotCompatibleLicense:
                    outputPackageInformationNotCompatibleInboundLicenseGitHub = "License " + InboundNotCompatibleLicense + \
                        " declared in GitHub found in " + packageName + " v. " + packageVersion + "."
                    outputPackageInformationNotCompatibleInboundLicenseGitHub = (
                        f'License {InboundNotCompatibleLicense}, declared in GitHub, found in {packageName} '
                        f'v. {packageVersion}.')
                    assessment[j]["packageInformation"] = outputPackageInformationNotCompatibleInboundLicenseGitHub
            assessment[j]["licenseViolation"] = outputNotCompatibleInboundLicense
            j += 1
    if len(assessment) == 0:
        assessment[j] = {}
        output = "Licensing issues at the package level have not been found"
        assessment[j]["noLicensesIssues"] = output
    return assessment


def parse_license_declared(licenses):
    licenseDeclaredReport = {}
    i = 0  # assessment index
    for i in licenses:
        licenseDeclaredReport[i] = {}
        if licenses[i].get("PyPILicenseSPDX"):
            licenseDeclaredReport[i]["License declared"] = (licenses[i].get("packageName") + " v." +
                                                            licenses[i].get("packageVersion")
                                                            + " has been declared with " +
                                                            licenses[i].get("PyPILicenseSPDX") + ", on PyPI.org.")
        else:
            if licenses[i].get("GitHubLicense"):
                licenseDeclaredReport[i]["License declared"] = (licenses[i].get("packageName") + " v." +
                                                                licenses[i].get("packageVersion")
                                                                + " has been declared with " +
                                                                licenses[i].get("GitHubLicense") + ", on GitHub API.")
        i += 1
    return licenseDeclaredReport
