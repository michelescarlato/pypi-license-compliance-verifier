from fpdf import FPDF


class ReportToPDF:

    @staticmethod
    def report_to_pdf(report, package_name):
        """Save the final report of the analysis in a pdf-file."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'U', size=15)
        pdf.cell(200, 10, txt=f'Analysis report: {package_name}', ln=1, align='C')
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(200, 5, txt=report, align='C')
        pdf.output(f'report-{package_name}.pdf')
        print(f'Report written in file \'report-{package_name}.pdf\'')
