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
        self._add_title(report_title)

    def _add_title(self, text):
        # function to add title for paragraph
        title = Paragraph(text, self.styles['Title'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.5 * inch))

    def add_heading(self, text, level='Heading2'):
        # function to add heading
        self.story.append(Paragraph(text, self.styles[level]))
        self.story.append(Spacer(1, 0.1 * inch))

    def create_table(self, data, col_widths=None):
        if not col_widths:
            col_widths = [2.5 * inch, 2.5 * inch]

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.steelblue), 
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        t = Table(data, colWidths=col_widths, rowHeights=None)
        t.setStyle(table_style)
        self.story.append(t)
        self.story.append(Spacer(1, 0.4 * inch))

    def stats_section(self, stats_dict):
        # averages of columns such as flowrate etc, pressure etc.
        self.add_heading("Field Statistics")
        for col, metrics in stats_dict.items():
            self.story.append(Paragraph(f"Field: {col}", self.styles['Heading3']))
            
            table_data = [["Metric", "Value"]]
            for m_name, val in metrics.items():
                formatted_val = f"{val:.2f}" if isinstance(val, (int, float)) else str(val)
                table_data.append([str(m_name), formatted_val])
            
            self.create_table(table_data)

    def equip_dist_section(self, dist_dict):
        # frequency of each equipment type
        self.add_heading("Equipment Type Distribution")
        table_data = [["Equipment Type", "Count"]]
        for category, count in dist_dict.items():
            table_data.append([str(category), str(count)])
        self.create_table(table_data)
    
    def equipment_averages_section(self, equipment_averages):
        # mean value of each parameter for each equipment 
        if not equipment_averages:
            return
        
        self.add_heading("Mean Values by Equipment Category")
        
        for equipment_type, field_averages in equipment_averages.items():
            self.story.append(Paragraph(f"Equipment Category: {equipment_type}", self.styles['Heading3']))
            table_data = [["Field", "Average Value"]]
            
            for field, avg_value in field_averages.items():
                formatted_avg = f"{avg_value:.2f}" if isinstance(avg_value, (int, float)) else str(avg_value)
                table_data.append([str(field), formatted_avg])
            
            self.create_table(table_data)

    def chart_section(self, chart_paths):
        # visualization section 
        if not chart_paths:
            return
            
        self.story.append(PageBreak())
        self.add_heading("Analysis Visualizations", 'Heading1')
        
        for path in chart_paths:
            img = Image(path, width=5.8 * inch, height=3.2 * inch)
            self.story.append(img)
            self.story.append(Spacer(1, 0.3 * inch))

    def build(self):
        self.doc.build(self.story)

def pdf_report(output_file, data_summary, chart_files):
    report = ReportGenerator(output_file, "Chemical Equipment Analysis Report")
    
    report.add_heading("Processing Summary")
    report.create_table([
        ["Metric", "Result"],
        ["Total Records Processed", str(data_summary.get('total_rows', 0))],
        ["Analysis Status", "Completed Successfully"]
    ])

    # averages of columns such as flowrate etc, pressure etc.
    if 'stats' in data_summary:
        report.stats_section(data_summary['stats'])

    # frequency of each equipment type
    if 'equip_dist' in data_summary:
        report.equip_dist_section(data_summary['equip_dist'])
    
    # mean value of each parameter for each equipment 
    if 'equip_averages' in data_summary:
        report.equipment_averages_section(data_summary['equip_averages'])
    
    # visualization section 
    if chart_files:
        report.chart_section(chart_files)
    
    report.build()