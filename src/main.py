import argparse
from executePypiResolver import ExecutePypiResolver
from licensesAnalysis import licenses_analysis
from reportToPDF import ReportToPDF


def main():
    parser = argparse.ArgumentParser(prog='PyPI-plugin')
    parser.add_argument("--product", type=str, help="Package name")
    parser.add_argument("--requirements", type=str, help="Path to the requirements file")
    parser.add_argument("--spdx_license", type=str, help="SPDX id of the license declared for this project")
    args = parser.parse_args()

    lcv_url = 'http://localhost:3251/'

    package_list = ExecutePypiResolver.execute_pypi_resolver_for_licensing(args.requirements)
    licensing_analysis_report = licenses_analysis(args, package_list, lcv_url)
    ReportToPDF.report_to_pdf(licensing_analysis_report, args.product)


if __name__ == "__main__":
    main()
