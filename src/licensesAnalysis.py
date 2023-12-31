from retrieveLocallyLicensesInformation import ReceiveLocallyLicensesInformation
from licenseComplianceVerification import (generate_inbound_license_set, parse_lcv_assessment_response,
                                           parse_license_declared)
from lcvlib.verify import compare_osadl
'''
* SPDX-FileCopyrightText: 2023 Michele Scarlato
*
* SPDX-License-Identifier: Apache-2.0
'''


def licenses_analysis(args, package_list):
    print("Start license analysis...")
    index = 0
    licenses_retrieved = ReceiveLocallyLicensesInformation.receive_locally_licenses_information(package_list, index)
    inbound_licenses = generate_inbound_license_set(licenses_retrieved)
    outbound_license = args.spdx_license
    lcv_assessment_response = compare_osadl(inbound_licenses, outbound_license)
    license_report = parse_lcv_assessment_response(lcv_assessment_response, licenses_retrieved)
    license_declared_report = parse_license_declared(licenses_retrieved)
    full_report = "Report about licenses:\n"
    if len(license_report) > 0:
        for i in license_report:
            if "noLicensesIssues" in license_report[i]:
                full_report += license_report[i]["noLicensesIssues"]
            else:
                full_report += "\n" + "############# - License violation against the declared Outbound license, number " + str(i + 1) + " #################\n" + "\n" + str(license_report[i]["packageInformation"]) + "\n" + str(license_report[i]["licenseViolation"])
    full_report += "\n\n############# - Licenses considered for the compliance verification: ############# \n"

    for i in license_declared_report:
        if "License declared" in license_declared_report[i]:
            full_report += license_declared_report[i]["License declared"]+"\n"
    print("License analysis done.")

    return full_report
