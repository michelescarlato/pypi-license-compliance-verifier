import argparse
from createDependenciesTree import DependenciesTree
from executePypiResolver import ExecutePypiResolver
from licensesAnalysis import licenses_analysis
from reportToPDF import ReportToPDF


def main():
    parser = argparse.ArgumentParser(prog='PyPI-plugin')
    parser.add_argument("--product", type=str, help="Package name")
    parser.add_argument("--requirements", type=str, help="Path to the requirements file")
    parser.add_argument("--spdx_license", type=str, help="SPDX id of the license declared for this project")
    args = parser.parse_args()
    dependencies_tree = DependenciesTree.create_dependencies_tree(args.requirements, args.product)
    dependencies_tree_with_licenses = DependenciesTree.increase_dependency_tree_with_license_information(dependencies_tree.name)
    package_list = ExecutePypiResolver.execute_pypi_resolver_for_licensing(args.requirements)
    licensing_analysis_report = licenses_analysis(args, package_list)
    ReportToPDF.report_to_pdf(licensing_analysis_report, args.product)


if __name__ == "__main__":
    main()
