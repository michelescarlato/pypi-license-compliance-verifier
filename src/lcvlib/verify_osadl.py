import pandas as pd
import json
from .SPDXIdMapping import IsAnSPDX


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
    def verify_osadl_matrix(inbound_licenses_cleaned, outbound_license, outbound_license_alias):
        verificationList = list()
        keys = ["message", "status", "inbound", "outbound", "inbound_SPDX", "outbound_SPDX"]
        dictOutput = dict.fromkeys(keys, None)
        print(inbound_licenses_cleaned)
        print(outbound_license)
        for inbound_license in inbound_licenses_cleaned:  # remove unsupported inbound_licenses
            if inbound_license not in supported_licenses_OSADL:
                print()
                output = "The inbound license " + str(inbound_license) + " is not present in the Compatibility Matrix"
                dictOutput['message'] = output
                dictOutput['status'] = "unknown"
                dictOutput['inbound'] = str(inbound_license)
                if IsAnSPDX(inbound_license):
                    dictOutput['inbound_SPDX'] = inbound_license
                dictOutput['outbound_SPDX'] = outbound_license
                dictOutput['outbound'] = outbound_license_alias
                verificationList.append(dictOutput)
                dictOutput = dict.fromkeys(keys, None)
                inbound_licenses_cleaned.remove(inbound_license)
                print(f"Removed: {inbound_license}")
                print("InboundLicenses_cleaned")
                print(inbound_licenses_cleaned)
        if outbound_license in supported_licenses_OSADL:
            column_names_list = inbound_licenses_cleaned.copy()
            column_names_list.insert(0, 'Compatibility')
            print("InboundLicenses_cleaned after column list assignation")
            print(inbound_licenses_cleaned)
            csv_file_path = "lcvlib/csv/OSADL_matrix.csv"
            print(f'Column_names_list: {column_names_list}')
            print(f'Inbound license: {inbound_licenses_cleaned}')
            matrix = pd.read_csv(csv_file_path, usecols=column_names_list)
            matrix = matrix.set_index('Compatibility')
            if (len(inbound_licenses_cleaned) == 1) and (inbound_licenses_cleaned[0] == outbound_license):
                output = "For this project only " + \
                    inbound_licenses_cleaned[0] + \
                    " as the inbound license has been detected, and it is the same of the outbound license (" + \
                    outbound_license_alias+("), implying that it is compatible. "
                                            "\nIt means that it is license compliant. ")
                verificationList.append(output)
                return verificationList
            for inbound_license in inbound_licenses_cleaned:
                comparison = matrix.loc[outbound_license, inbound_license]
                print(f'Outbound license: {outbound_license}, inbound license:'
                      f' {inbound_license}, comparison: {comparison}')
                if comparison == "No":
                    output = str(inbound_license)+" is not compatible with " + \
                        outbound_license_alias+" as an outbound license."
                    dictOutput['status'] = "not compatible"
                if comparison == "Yes":
                    output = str(inbound_license)+" is compatible with " + \
                        outbound_license_alias + " as an outbound license."
                    dictOutput['status'] = "compatible"
                # OSADL Matrix could be shipped with empty field, resulting in nan.
                if comparison == "Same":
                    output = str(inbound_license)+" is compatible with " + \
                        outbound_license_alias + " as an outbound license."
                    dictOutput['status'] = "compatible"
                if comparison == "Unknown":
                    output = ("There is insufficient information or knowledge whether the "+str(inbound_license) +
                              " as inbound license" + " is compatible with the " + outbound_license_alias +
                              " as outbound license. Therefore a general recommendation" +
                              " on the compatibility of "+str(inbound_license)+" as inbound with the " +
                              outbound_license+" as outbound cannot be given.")
                    dictOutput['status'] = "insufficient information"
                if comparison == "Check dependency":
                    output = "Depending compatibility of the "+str(inbound_license)+" with the " + \
                        outbound_license_alias + " license is explicitly stated in the " + \
                        outbound_license_alias+" license checklist hosted by OSADL.org"
                    dictOutput['status'] = "Depending on the use case"
                dictOutput['message'] = output
                dictOutput['inbound'] = str(inbound_license)
                dictOutput['inbound_SPDX'] = inbound_license
                dictOutput['outbound_SPDX'] = outbound_license
                dictOutput['outbound'] = outbound_license_alias
                verificationList.append(dictOutput)
                dictOutput = dict.fromkeys(keys, None)
        return verificationList

    @staticmethod
    def verify_osadl_json(inbound_licenses_cleaned, outbound_license, outbound_license_alias):
        verificationList = list()
        keys = ["message", "status", "inbound", "outbound", "inbound_SPDX", "outbound_SPDX"]
        dictOutput = dict.fromkeys(keys, None)
        print(inbound_licenses_cleaned)
        print(outbound_license)
        with open("lcvlib/matrixseqexpl.json", "r") as file:
            jsonData = json.load(file)
        for inbound_license in inbound_licenses_cleaned:  # remove unsupported inbound_licenses
            if inbound_license not in supported_licenses_OSADL:
                print()
                output = "The inbound license " + str(inbound_license) + " is not present in the Compatibility Matrix"
                dictOutput['message'] = output
                dictOutput['status'] = "unknown"
                dictOutput['inbound'] = str(inbound_license)
                if IsAnSPDX(inbound_license):
                    dictOutput['inbound_SPDX'] = inbound_license
                dictOutput['outbound_SPDX'] = outbound_license
                dictOutput['outbound'] = outbound_license_alias
                verificationList.append(dictOutput)
                dictOutput = dict.fromkeys(keys, None)
                inbound_licenses_cleaned.remove(inbound_license)
                print(f"Removed: {inbound_license}")
                print("InboundLicenses_cleaned")
                print(inbound_licenses_cleaned)
        if outbound_license in supported_licenses_OSADL:
            if (len(inbound_licenses_cleaned) == 1) and (inbound_licenses_cleaned[0] == outbound_license):
                output = "For this project only " + \
                    inbound_licenses_cleaned[0] + \
                    " as the inbound license has been detected, and it is the same of the outbound license (" + \
                    outbound_license_alias+("), implying that it is compatible. "
                                            "\nIt means that it is license compliant. ")
                verificationList.append(output)
                return verificationList
            for inbound_license in inbound_licenses_cleaned:
                print(f'Outbound license: {outbound_license}, inbound license: {inbound_license}')
                for outbound_license in jsonData['licenses']:
                    if outbound_license["name"] == outbound_license:
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
                                dictOutput['outbound_SPDX'] = outbound_license
                                dictOutput['outbound'] = outbound_license_alias
                                verificationList.append(dictOutput)
                                dictOutput = dict.fromkeys(keys, None)
        return verificationList
