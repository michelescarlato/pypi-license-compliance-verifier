import requests
import pandas as pd
import json
from .SPDXIdMapping import ConvertToSPDX, IsAnSPDX


'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''

# get the list of Matrix supported licenses
df = pd.read_csv('lcvlib/csv/OSADL_matrix.csv', index_col=0)  # verify.py is tight to the main.py execution -
# the csv path is relative to where the main.py is.
supported_licenses_OSADL = list(df.index)  # create a list of licenses presents in the OSADL matrix


class OSADLVerification:
    @staticmethod
    def verify_osadl_matrix(InboundLicenses_cleaned, OutboundLicense, OutboundLicenseAlias):
        verificationList = list()
        keys = ["message", "status", "inbound", "outbound", "inbound_SPDX", "outbound_SPDX"]
        dictOutput = dict.fromkeys(keys, None)
        print(InboundLicenses_cleaned)
        print(OutboundLicense)
        for inbound_license in InboundLicenses_cleaned:  # remove unsupported inbound_licenses
            if inbound_license not in supported_licenses_OSADL:
                print()
                output = "The inbound license " + str(inbound_license) + " is not present in the Compatibility Matrix"
                dictOutput['message'] = output
                dictOutput['status'] = "unknown"
                dictOutput['inbound'] = str(inbound_license)
                if IsAnSPDX(inbound_license):
                    dictOutput['inbound_SPDX'] = inbound_license
                dictOutput['outbound_SPDX'] = OutboundLicense
                dictOutput['outbound'] = OutboundLicenseAlias
                verificationList.append(dictOutput)
                dictOutput = dict.fromkeys(keys, None)
                InboundLicenses_cleaned.remove(inbound_license)
                print(f"Removed: {inbound_license}")
                print("InboundLicenses_cleaned")
                print(InboundLicenses_cleaned)
        if OutboundLicense in supported_licenses_OSADL:
            column_names_list = InboundLicenses_cleaned.copy()
            column_names_list.insert(0, 'Compatibility')
            print("InboundLicenses_cleaned after column list assignation")
            print(InboundLicenses_cleaned)
            csv_file_path = "lcvlib/csv/OSADL_matrix.csv"
            print(f'Column_names_list: {column_names_list}')
            print(f'Inbound license: {InboundLicenses_cleaned}')
            df = pd.read_csv(csv_file_path, usecols=column_names_list)
            df = df.set_index('Compatibility')
            if (len(InboundLicenses_cleaned) == 1) and (InboundLicenses_cleaned[0] == OutboundLicense):
                output = "For this project only " + \
                    InboundLicenses_cleaned[0] + \
                    " as the inbound license has been detected, and it is the same of the outbound license (" + \
                    OutboundLicenseAlias+"), implying that it is compatible. \nIt means that it is license compliant. "
                verificationList.append(output)
                return verificationList
            for inbound_license in InboundLicenses_cleaned:
                # comparison = df.loc[license, OutboundLicense]  # I guess reverting this, we can read OSADL_matrix.csv
                # new version would be:
                print(f'Outbound license: {OutboundLicense}, inbound license: {inbound_license}')
                comparison = df.loc[OutboundLicense, inbound_license]
                print("comparison:")
                print(comparison)
                if comparison == "No":
                    output = str(inbound_license)+" is not compatible with " + \
                        OutboundLicenseAlias+" as an outbound license."
                    dictOutput['status'] = "not compatible"
                if comparison == "Yes":
                    output = str(inbound_license)+" is compatible with " + \
                        OutboundLicenseAlias + " as an outbound license."
                    dictOutput['status'] = "compatible"
                # OSADL Matrix could be shipped with empty field, resulting in nan.
                if comparison == "Same":
                    output = str(inbound_license)+" is compatible with " + \
                        OutboundLicenseAlias + " as an outbound license."
                    dictOutput['status'] = "compatible"
                if comparison == "Unknown":
                    output = "There is insufficient information or knowledge whether the "+str(inbound_license)+" as inbound license" + \
                        " is compatible with the " + OutboundLicenseAlias + " as outbound license. Therefore a general recommendation" + \
                        " on the compatibility of "+str(inbound_license)+" as inbound with the " + \
                        OutboundLicense+" as outbound cannot be given."
                    dictOutput['status'] = "insufficient information"
                if comparison == "Check dependency":
                    output = "Depending compatibility of the "+str(inbound_license)+" with the " + \
                        OutboundLicenseAlias + " license is explicitly stated in the " + \
                        OutboundLicenseAlias+" license checklist hosted by OSADL.org"
                    dictOutput['status'] = "Depending on the use case"
                dictOutput['message'] = output
                dictOutput['inbound'] = str(inbound_license)
                dictOutput['inbound_SPDX'] = inbound_license
                dictOutput['outbound_SPDX'] = OutboundLicense
                dictOutput['outbound'] = OutboundLicenseAlias
                verificationList.append(dictOutput)
                dictOutput = dict.fromkeys(keys, None)
        return verificationList


    @staticmethod
    def verify_osadl_json(InboundLicenses_cleaned, OutboundLicense, OutboundLicenseAlias):
        verificationList = list()
        keys = ["message", "status", "inbound", "outbound", "inbound_SPDX", "outbound_SPDX"]
        dictOutput = dict.fromkeys(keys, None)
        print(InboundLicenses_cleaned)
        print(OutboundLicense)
        with open("lcvlib/matrixseqexpl.json", "r") as file:
            jsonData = json.load(file)
        for inbound_license in InboundLicenses_cleaned:  # remove unsupported inbound_licenses
            if inbound_license not in supported_licenses_OSADL:
                print()
                output = "The inbound license " + str(inbound_license) + " is not present in the Compatibility Matrix"
                dictOutput['message'] = output
                dictOutput['status'] = "unknown"
                dictOutput['inbound'] = str(inbound_license)
                if IsAnSPDX(inbound_license):
                    dictOutput['inbound_SPDX'] = inbound_license
                dictOutput['outbound_SPDX'] = OutboundLicense
                dictOutput['outbound'] = OutboundLicenseAlias
                verificationList.append(dictOutput)
                dictOutput = dict.fromkeys(keys, None)
                InboundLicenses_cleaned.remove(inbound_license)
                print(f"Removed: {inbound_license}")
                print("InboundLicenses_cleaned")
                print(InboundLicenses_cleaned)
        if OutboundLicense in supported_licenses_OSADL:
            if (len(InboundLicenses_cleaned) == 1) and (InboundLicenses_cleaned[0] == OutboundLicense):
                output = "For this project only " + \
                    InboundLicenses_cleaned[0] + \
                    " as the inbound license has been detected, and it is the same of the outbound license (" + \
                    OutboundLicenseAlias+"), implying that it is compatible. \nIt means that it is license compliant. "
                verificationList.append(output)
                return verificationList
            for inbound_license in InboundLicenses_cleaned:
                print(f'Outbound license: {OutboundLicense}, inbound license: {inbound_license}')
                for outbound_license in jsonData['licenses']:
                    if outbound_license["name"] == OutboundLicense:
                        print(outbound_license["name"])
                        for inbound_license_json_element in outbound_license["compatibilities"]:
                            if inbound_license_json_element["name"] == inbound_license:
                                print(inbound_license_json_element["name"])
                                comparison = inbound_license_json_element["compatibility"]
                                output = inbound_license_json_element["explanation"]
                                if comparison == "No":
                                    dictOutput['status'] = "not compatible"
                                if comparison == "Yes":
                                    dictOutput['status'] = "compatible"
                                # OSADL Matrix could be shipped with empty field, resulting in nan.
                                if comparison == "Same":
                                    dictOutput['status'] = "compatible"
                                if comparison == "Unknown":
                                    dictOutput['status'] = "insufficient information"
                                if comparison == "Check dependency":
                                    dictOutput['status'] = "Depending on the use case"
                                dictOutput['message'] = output
                                dictOutput['inbound'] = str(inbound_license)
                                dictOutput['inbound_SPDX'] = inbound_license
                                dictOutput['outbound_SPDX'] = OutboundLicense
                                dictOutput['outbound'] = OutboundLicenseAlias
                                verificationList.append(dictOutput)
                                dictOutput = dict.fromkeys(keys, None)
        return verificationList