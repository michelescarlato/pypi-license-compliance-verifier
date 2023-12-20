# pypi-license-compliance-verifier

The `pypi license compliance verifier` is a standalone version resulting from a combination 
of the [python license detector](https://github.com/fasten-project/fasten/tree/main/analyzer/python-license-detector)
and the [license and compliance verifier](https://github.com/michelescarlato/LicenseComplianceVerifier).

It aims at providing an Open Source licensing assessment of the direct and transitive dependencies.

## Usage

1. Clone the repository.

2. (optional) create a virtual environment

3. e.g.
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the dependencies with:

```bash
pip3 -r install requirements.txt
```

5. Put the requirements.txt that you want to analyze inside a path, and specify it in the cli arguments:

```bash
cd src
python3 main.py --requirements pypi-lcv/requirements_example.txt --spdx_license=Apache2.0 --product=pypi-lcv
```

The above requirements.txt will perform a compliance assessment of this tool.

Note: the `pipdeptree` dependencies tree resolution provides a deeper dependency resolution than the [pypi-resolver](https://pypi.org/project/pypi-resolver/)'s one.
Currently, the license compliance verification assessment is made upon the dependency resolved by the pypi-resolver.
As a work in progress, a license compliance verification will be performed upon the dependencies resolution provided by 
`pipdeptree`. 
Anyway, at the current stage, the pypi license compliance verifier increases the json produced by pipdeptree with license information.
The augmented json will be stored in `src/<args.product>/dependencies_tree_with_licenses.json`, where `args.product` is the product `name` given as the `--product=name`.
The augmented json provides an interesting insight of the imported licenses.