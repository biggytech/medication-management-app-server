import os
import tempfile
from datetime import datetime, date
from typing import Dict, List, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from models.user.user import User
from models.medication_log.medication_log import MedicationLog
from models.health_tracker_log.health_tracker_log import HealthTrackerLog
from models.medicine.medicine import Medicine
from models.health_tracker.health_tracker import HealthTracker


class PatientReportGenerator:
    """Generates professional medical reports for patients"""
    
    def __init__(self, language: str = "en-US"):
        self.language = language
        self.translations = self._get_translations()
        
    def _get_translations(self) -> Dict[str, Dict[str, str]]:
        """Get translations for different languages"""
        return {
            "en-US": {
                "title": "Patient Medical Report",
                "patient_info": "Patient Information",
                "name": "Name",
                "date_of_birth": "Date of Birth",
                "age": "Age",
                "sex": "Sex",
                "male": "Male",
                "female": "Female",
                "report_period": "Report Period",
                "from": "From",
                "to": "To",
                "medication_summary": "Medication Summary",
                "medication_name": "Medication",
                "form": "Form",
                "taken": "Taken",
                "skipped": "Skipped",
                "total": "Total",
                "compliance_rate": "Compliance Rate",
                "health_tracker_summary": "Health Tracker Summary",
                "tracker_type": "Tracker Type",
                "entries": "Entries",
                "average_value": "Average Value",
                "blood_pressure": "Blood Pressure",
                "heart_rate": "Heart Rate",
                "weight": "Weight",
                "body_temperature": "Body Temperature",
                "menstrual_cycle": "Menstrual Cycle",
                "generated_on": "Generated on",
                "page": "Page",
                "of": "of"
            },
            "ru-RU": {
                "title": "Медицинский отчет пациента",
                "patient_info": "Информация о пациенте",
                "name": "Имя",
                "date_of_birth": "Дата рождения",
                "age": "Возраст",
                "sex": "Пол",
                "male": "Мужской",
                "female": "Женский",
                "report_period": "Период отчета",
                "from": "С",
                "to": "По",
                "medication_summary": "Сводка по лекарствам",
                "medication_name": "Лекарство",
                "form": "Форма",
                "taken": "Принято",
                "skipped": "Пропущено",
                "total": "Всего",
                "compliance_rate": "Соблюдение режима",
                "health_tracker_summary": "Сводка по показателям здоровья",
                "tracker_type": "Тип показателя",
                "entries": "Записи",
                "average_value": "Среднее значение",
                "blood_pressure": "Артериальное давление",
                "heart_rate": "Частота сердечных сокращений",
                "weight": "Вес",
                "body_temperature": "Температура тела",
                "menstrual_cycle": "Менструальный цикл",
                "generated_on": "Создано",
                "page": "Страница",
                "of": "из"
            }
        }
    
    def _t(self, key: str) -> str:
        """Get translation for current language"""
        return self.translations.get(self.language, self.translations["en-US"]).get(key, key)
    
    def _calculate_age(self, date_of_birth: date) -> int:
        """Calculate age from date of birth"""
        today = date.today()
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    
    def _format_date(self, date_obj: datetime) -> str:
        """Format date according to language"""
        if self.language == "ru-RU":
            return date_obj.strftime("%d.%m.%Y")
        else:
            return date_obj.strftime("%m/%d/%Y")
    
    def _get_sex_translation(self, sex: str) -> str:
        """Get translated sex value"""
        if sex == "male":
            return self._t("male")
        elif sex == "female":
            return self._t("female")
        return sex
    
    def _get_tracker_type_translation(self, tracker_type: str) -> str:
        """Get translated tracker type"""
        type_mapping = {
            "blood_pressure": self._t("blood_pressure"),
            "heart_rate": self._t("heart_rate"),
            "weight": self._t("weight"),
            "body_temperature": self._t("body_temperature"),
            "menstrual_cycle": self._t("menstrual_cycle")
        }
        return type_mapping.get(tracker_type, tracker_type)
    
    def _create_header_footer(self, canvas, doc):
        """Create header and footer for each page"""
        canvas.saveState()
        
        # Header
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawCentredString(letter[0]/2, letter[1]-50, self._t("title"))
        
        # Footer with page number
        canvas.setFont("Helvetica", 10)
        page_num = canvas.getPageNumber()
        canvas.drawRightString(letter[0]-50, 50, f"{self._t('page')} {page_num}")
        
        canvas.restoreState()
    
    def generate_report(self, user: User, medication_logs: List[MedicationLog], 
                       health_tracker_logs: List[HealthTrackerLog], 
                       start_date: datetime, end_date: datetime) -> str:
        """Generate PDF report and return file path"""
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.close()
        
        # Create PDF document
        doc = SimpleDocTemplate(temp_file.name, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph(self._t("title"), title_style))
        story.append(Spacer(1, 20))
        
        # Patient Information
        story.append(Paragraph(self._t("patient_info"), heading_style))
        
        # Calculate age
        age = self._calculate_age(user.date_of_birth) if user.date_of_birth else "N/A"
        
        patient_data = [
            [self._t("name"), user.full_name],
            [self._t("date_of_birth"), self._format_date(user.date_of_birth) if user.date_of_birth else "N/A"],
            [self._t("age"), str(age)],
            [self._t("sex"), self._get_sex_translation(user.sex) if user.sex else "N/A"]
        ]
        
        patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(patient_table)
        story.append(Spacer(1, 20))
        
        # Report Period
        story.append(Paragraph(self._t("report_period"), heading_style))
        period_data = [
            [self._t("from"), self._format_date(start_date)],
            [self._t("to"), self._format_date(end_date)]
        ]
        
        period_table = Table(period_data, colWidths=[2*inch, 4*inch])
        period_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(period_table)
        story.append(Spacer(1, 20))
        
        # Medication Summary
        story.append(Paragraph(self._t("medication_summary"), heading_style))
        
        # Process medication data
        medication_stats = {}
        for log in medication_logs:
            medicine = log.medicine
            if medicine.title not in medication_stats:
                medication_stats[medicine.title] = {
                    'form': medicine.form,
                    'taken': 0,
                    'skipped': 0
                }
            
            if log.type == 'taken':
                medication_stats[medicine.title]['taken'] += 1
            elif log.type == 'skipped':
                medication_stats[medicine.title]['skipped'] += 1
        
        # Create medication table
        if medication_stats:
            med_data = [[self._t("medication_name"), self._t("form"), self._t("taken"), self._t("skipped"), self._t("total"), self._t("compliance_rate")]]
            
            for medicine_name, stats in medication_stats.items():
                total = stats['taken'] + stats['skipped']
                compliance_rate = f"{(stats['taken'] / total * 100):.1f}%" if total > 0 else "0%"
                med_data.append([
                    medicine_name,
                    stats['form'],
                    str(stats['taken']),
                    str(stats['skipped']),
                    str(total),
                    compliance_rate
                ])
            
            med_table = Table(med_data, colWidths=[1.5*inch, 1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch])
            med_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(med_table)
        else:
            story.append(Paragraph("No medication data available for this period.", styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Health Tracker Summary
        story.append(Paragraph(self._t("health_tracker_summary"), heading_style))
        
        # Process health tracker data
        tracker_stats = {}
        for log in health_tracker_logs:
            tracker = log.health_tracker
            tracker_type = self._get_tracker_type_translation(tracker.type)
            
            if tracker_type not in tracker_stats:
                tracker_stats[tracker_type] = {
                    'entries': 0,
                    'total_value1': 0,
                    'total_value2': 0,
                    'has_value2': False
                }
            
            tracker_stats[tracker_type]['entries'] += 1
            tracker_stats[tracker_type]['total_value1'] += log.value1
            if log.value2 is not None:
                tracker_stats[tracker_type]['total_value2'] += log.value2
                tracker_stats[tracker_type]['has_value2'] = True
        
        # Create health tracker table
        if tracker_stats:
            tracker_data = [[self._t("tracker_type"), self._t("entries"), self._t("average_value")]]
            
            for tracker_type, stats in tracker_stats.items():
                avg_value1 = stats['total_value1'] / stats['entries'] if stats['entries'] > 0 else 0
                avg_value2 = stats['total_value2'] / stats['entries'] if stats['entries'] > 0 and stats['has_value2'] else None
                
                if avg_value2 is not None:
                    avg_value_str = f"{avg_value1:.1f} / {avg_value2:.1f}"
                else:
                    avg_value_str = f"{avg_value1:.1f}"
                
                tracker_data.append([
                    tracker_type,
                    str(stats['entries']),
                    avg_value_str
                ])
            
            tracker_table = Table(tracker_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
            tracker_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(tracker_table)
        else:
            story.append(Paragraph("No health tracker data available for this period.", styles['Normal']))
        
        # Add generation timestamp
        story.append(Spacer(1, 30))
        story.append(Paragraph(f"{self._t('generated_on')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                             styles['Normal']))
        
        # Build PDF
        doc.build(story, onFirstPage=self._create_header_footer, onLaterPages=self._create_header_footer)
        
        return temp_file.name
