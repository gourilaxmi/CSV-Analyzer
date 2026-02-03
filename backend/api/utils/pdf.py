from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

class ReportGenerator:
    
    def __init__(self, filename, report_title="Report"):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.story = [] 

        self.title(report_title)

    def title(self, text):
        title = Paragraph(text, self.styles['Title'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.5 * inch))

    def summary_table(self, metrics, section_name="Summary"):
        self.story.append(Paragraph(section_name, self.styles['Heading2']))
        
        table_data = [["Metric", "Result"]] 
        table_data.extend([[key, str(val)] for key, val in metrics.items()])

        modern_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#33475b')), 
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])

        summary_table = Table(table_data, colWidths=[2.5 * inch, 2.5 * inch])
        summary_table.setStyle(modern_style)
        
        self.story.append(summary_table)
        self.story.append(Spacer(1, 0.4 * inch))

    def chart(self, chart_paths):
        self.story.append(PageBreak())
        self.story.append(Paragraph("Visualizations", self.styles['Heading1']))
        self.story.append(Spacer(1, 0.2 * inch))

        for path in chart_paths:
            if path:
                img = Image(path, width=6 * inch, height=3.5 * inch)
                self.story.append(img)
                self.story.append(Spacer(1, 0.3 * inch))

    def create(self):
        self.doc.build(self.story)
        print(f"Successfully generated: {self.filename}")

def pdf_report(output_file, data_summary, chart_files):

    report = ReportGenerator(output_file, "Chemical Equipment Analysis")
    
    report.summary_table(
        metrics={"Total Records": data_summary.get('total_rows', 0)}, 
        section_name="Statistics"
    )
    
    if chart_files:
        report.chart(chart_files)
    
    report.create()