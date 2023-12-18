# Copyright (c) 2018-2020 FASTEN.
#
# This file is part of FASTEN
# (see https://www.fasten-project.eu/).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import subprocess as sp
import os
from pkginfo import Wheel, SDist, BDist


TMP_DIR = "/tmp"
TMP_REQUIREMENTS_TXT = "temp.txt"


def create_requirements_file(requirements):
    with open(TMP_REQUIREMENTS_TXT, 'w') as f:
        for item in requirements:
            f.write("%s\n" % item)


def delete_requirements_file():
    if os.path.exists(TMP_REQUIREMENTS_TXT):
        os.remove(TMP_REQUIREMENTS_TXT)


def get_response(input_string, resolution_status, resolution_result):
    res = {"input": input_string, "status": resolution_status}
    if resolution_status:
        res['packages'] = {}
        for package, version in resolution_result:
            if package:
                res['packages'][package] = {
                    "package": package,
                    "version": version
                }
    else:
        res['error'] = resolution_result
    return res


def get_response_for_api(resolution_status, resolution_result):
    res = {}
    if resolution_status:
        list1 = []
        for package, version in resolution_result:
            if package:
                list1.append({
                    "product": package,
                    "version": version
                })
        res = list1
    else:
        res['error'] = resolution_result
    return res


def parse_file(path):
    w = None
    package = None
    version = None
    if path.endswith(".tar.gz"):
        w = SDist(path)
    if path.endswith(".egg"):
        w = BDist(path)
    if path.endswith(".whl"):
        w = Wheel(path)
    if w:
        package = w.name
        version = w.version

    return package, version


def run_pip(input_string, is_local_resolution):
    res = set()
    if is_local_resolution:
        pip_options = [
            "pip3", "download",
            "-r", input_string,
            "-d", TMP_DIR
        ]
    else:
        pip_options = [
            "pip3", "download",
            input_string.replace("=", "=="),
            "-d", TMP_DIR
        ]
    cmd = sp.Popen(pip_options, stdout=sp.PIPE, stderr=sp.STDOUT)
    stdout, _ = cmd.communicate()
    stdout = stdout.decode("utf-8").splitlines()
    err = None
    # package = None
    for line in stdout:
        print(line)
        if line.startswith("ERROR"):
            err = line
            break
        fname = None
        if "Downloading" in line:
            fname = os.path.join(TMP_DIR, os.path.basename(line.split()[1]))
        elif "File was already downloaded" in line:
            fname = line.split()[4]
        if fname:
            try:
                res.add(parse_file(fname))
            except Exception as e:
                err = str(e)
                break
    if err:
        return False, err
    return True, res
