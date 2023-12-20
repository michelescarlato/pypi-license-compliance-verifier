import requests
import pandas as pd
from .SPDXIdMapping import ConvertToSPDX, IsAnSPDX
from .verify_osadl import OSADLVerification

'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''

# get the list of Matrix supported licenses
df = pd.read_csv('lcvlib/csv/OSADL_matrix.csv', index_col=0)
supported_licenses_OSADL = list(df.index)  # create a list of licenses presents in the OSADL matrix


def csv_to_dataframe(csv_file_path, column_names_list):
    """
    Import a CSV and transform it into a pandas dataframe selecting only the useful columns from the Compatibility Matrix
    """
    dataframe = pd.read_csv(csv_file_path, usecols=column_names_list)
    return dataframe


def compare_osadl(inbound_licenses, outbound_license):
    print(inbound_licenses)
    InboundLicenses_SPDX = []
    for inbound_license in inbound_licenses:
        if not IsAnSPDX(inbound_license):
            license_spdx = ConvertToSPDX(inbound_license)
            InboundLicenses_SPDX.append(license_spdx)
        else:
            InboundLicenses_SPDX.append(inbound_license)
    if not IsAnSPDX(outbound_license):
        OutboundLicense_SPDX = ConvertToSPDX(outbound_license)
        print("OutboundLicense_SPDX:")
        print(OutboundLicense_SPDX)
    else:
        OutboundLicense_SPDX = outbound_license

    if len(InboundLicenses_SPDX) == 1:
        print("The SPDX id for the only inbound license detected is:")
        print(InboundLicenses_SPDX[0])
    else:
        print("The SPDX IDs for the inbound licenses found are:")
        print(InboundLicenses_SPDX)
    print("#################")
    print("Running the license compliance verification:")
    print("Inbound license list :\n"+str(InboundLicenses_SPDX))
    print("The outbound license is: "+OutboundLicense_SPDX)
    csv_file_path = "lcvlib/csv/OSADL_matrix.csv"
    for inbound_license in inbound_licenses:
        if inbound_license not in supported_licenses_OSADL:
            inbound_licenses.remove(inbound_license)
    #verificationList = OSADLVerification.verify_osadl_matrix(
     #   InboundLicenses_SPDX, OutboundLicense_SPDX, OutboundLicense)
    verificationList = OSADLVerification.verify_osadl_json(
        InboundLicenses_SPDX, OutboundLicense_SPDX, outbound_license)
    verificationList = parse_verification_list(verificationList)
    return verificationList


def parse_verification_list(verification_list: dict):
    """
    Print at screen info useful for debugging.

    :param verification_list:
    :return:
    """
    indexLicense = 0
    for element in verification_list:
        #print("Element:")
        print(element)
        if element['status'] == 'compatible':
            #print('compatible in element')
            indexLicense += 1
    print(str(indexLicense)+" above "+str(len(verification_list))
          + " licenses found are compatible.")
    if indexLicense == len(verification_list):
        print("Hence your project is compatible.")
    else:
        print("Hence your project may not be compatible.")
    return verification_list
