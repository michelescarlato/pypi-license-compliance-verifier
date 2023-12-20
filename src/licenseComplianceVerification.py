"""
* SPDX-FileCopyrightText: 2023 Michele Scarlato
*
* SPDX-License-Identifier: Apache-2.0
"""


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
                    outputPackageInformationNotCompatibleInboundLicensePyPI = (
                            f'License {InboundNotCompatibleLicense}, declared in PyPI, found in {packageName} '
                            f'v. {packageVersion}.')
                    assessment[j]["packageInformation"] = outputPackageInformationNotCompatibleInboundLicensePyPI
                if licenses[i].get("GitHubLicense") == InboundNotCompatibleLicense:
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
    return licenseDeclaredReport
