# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.styles import GradientFill, PatternFill
from six import BytesIO
import io  # Add this import to resolve the NameError

from datetime import datetime
from datetime import datetime, timedelta
from frappe.utils import (getdate, cint, add_months, date_diff, add_days, format_date,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from openpyxl.drawing.image import Image as xlImage
import requests


# class SalaryRegisterReports(Document):
# 	pass


@frappe.whitelist()
def download():
    filename = 'Salary Register for Staff.xlsx'
    build_xlsx_response(filename)

def make_xlsx(sheet_name=None):
    args = frappe.local.form_dict
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name if sheet_name else 'Sheet1'
    
    data = get_data(args)
    
    if not data:  # Check if data is empty or None
        frappe.throw("No data available to generate the report.")
    
    
    image_url="http://157.245.101.198/files/JohokuNew.png"
    image_data = requests.get(image_url).content
    img = xlImage(io.BytesIO(image_data))
    img_cell = ws.cell(row=1, column=10)
    img.width = 100
    img.height = 80
    ws.add_image(img,"J1")
         
        
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=11)
    ws["L1"].value = "JOHOKU MANUFACTURING PRIVATE LIMITED"
    ws["L1"].alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    ws["L1"].font = Font(bold=True, size=14)
    ws["AT1"].value = "Prepared By"
    ws["Ay1"].value = "Checked By"
    ws["BC1"].value = "Verified By"
    ws["BH1"].value = "Approved By"
    ws.merge_cells(start_row=1, start_column=12, end_row=1, end_column=45)
    ws.merge_cells(start_row=1, start_column=46, end_row=1, end_column=50)
    ws.merge_cells(start_row=1, start_column=51, end_row=1, end_column=54)
    ws.merge_cells(start_row=1, start_column=55, end_row=1, end_column=59)
    ws.merge_cells(start_row=1, start_column=60, end_row=1, end_column=65)
    for row in data:
        if not isinstance(row, (list, tuple)):
            row = [row]  
        ws.append(row)
    # Merging cells based on the number of rows in the header first three rows
    # ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=12)
    # ws.merge_cells(start_row=1, start_column=13, end_row=1, end_column=44)
    # # ws["P1"].value = "JOHOKU MANUFACTURING PRIVATE LIMITED"
    
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=45)
    ws.merge_cells(start_row=2, start_column=46, end_row=3, end_column=50)
    ws.merge_cells(start_row=2, start_column=51, end_row=3, end_column=54)
    ws.merge_cells(start_row=2, start_column=55, end_row=3, end_column=59)
    ws.merge_cells(start_row=2, start_column=60, end_row=3, end_column=65)
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=45)
    for x in range(1,16):
        ws.merge_cells(start_row=4, start_column=x, end_row=5, end_column=x)
    for x in range(26,36):
        ws.merge_cells(start_row=4, start_column=x, end_row=5, end_column=x)
        
    ws.merge_cells(start_row=4, start_column=54, end_row=4, end_column=54)
    ws.merge_cells(start_row=4, start_column=65, end_row=5, end_column=65)
    ws.merge_cells(start_row=4, start_column=64, end_row=5, end_column=64)
    ws.merge_cells(start_row=4, start_column=16, end_row=4, end_column=25)
    ws.merge_cells(start_row=4, start_column=36, end_row=4, end_column=45)
    ws.merge_cells(start_row=4, start_column=46, end_row=4, end_column=48)
    ws.merge_cells(start_row=4, start_column=49, end_row=4, end_column=52)
    ws.merge_cells(start_row=4, start_column=56, end_row=4, end_column=63)
    ws.merge_cells(start_row=4, start_column=53, end_row=4, end_column=53)
    ws.merge_cells(start_row=4, start_column=55, end_row=5, end_column=55)
    # ws.merge_cells(start_row=4, start_column=55, end_row=4, end_column=64)

    apply_styles(ws)
    set_column_widths(ws)

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file

def apply_styles(ws):
    align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
    align_right = Alignment(horizontal='right', vertical='top', wrap_text=True)
    align_left = Alignment(horizontal='left', vertical='top', wrap_text=True)
    header_font = Font(bold=True, size=14)
    text_font = Font(bold=True, size=8)
    text_font_header = Font(bold=True, size=10)
    text_font_data = Font(bold=False, size=9)
    border = Border(
        left=Side(border_style='thin'),
        right=Side(border_style='thin'),
        top=Side(border_style='thin'),
        bottom=Side(border_style='thin')
    )
    for rows in ws.iter_rows(min_row=1, max_row=2, min_col=45, max_col=65):
        for cell in rows:
            cell.font = header_font
            cell.alignment = align_center
            cell.border = border
    for x in range(2,4):
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=1, max_col=65):
            for cell in rows:
                cell.font = header_font
                cell.alignment = align_center
                cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=5, min_col=1, max_col=16):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=5, min_col=26, max_col=35):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=5, min_col=55, max_col=55):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=5, min_col=64, max_col=65):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=4, min_col=16, max_col=25):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=4, min_col=36, max_col=45):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=4, min_col=41, max_col=41):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=4, min_col=46, max_col=48):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=5, min_col=49, max_col=54):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=4, min_col=56, max_col=63):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=4, min_col=53, max_col=53):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=4, min_col=54, max_col=54):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=5, min_col=55, max_col=55):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=4, max_row=4, min_col=49, max_col=52):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
   
    for x in range(16,26):
        for rows in ws.iter_rows(min_row=5, max_row=5, min_col=x, max_col=x):
            for cell in rows:
                cell.font = text_font_header
                cell.alignment = align_center
                cell.border = border
    for x in range(36,54):
        for rows in ws.iter_rows(min_row=5, max_row=5, min_col=x, max_col=x):
            for cell in rows:
                cell.font = text_font_header
                cell.alignment = align_center
                cell.border = border
    for x in range(55,63):
        for rows in ws.iter_rows(min_row=5, max_row=5, min_col=x, max_col=x):
            for cell in rows:
                cell.font = text_font_header
                cell.alignment = align_center
                cell.border = border
    for x in range(63,66):
        for rows in ws.iter_rows(min_row=4, max_row=5, min_col=x, max_col=x):
            for cell in rows:
                cell.font = text_font_header
                cell.alignment = align_center
                cell.border = border
    # for rows in ws.iter_rows(min_row=6, max_row=ws.max_row - 1, min_col=15, max_col=15):
    for x in range(6,ws.max_row + 1):
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=4, max_col=65):
            for cell in rows:
                cell.font = text_font_data
                cell.alignment = align_center
                cell.border = border
    for x in range(6,ws.max_row + 1):
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=3, max_col=3):
            for cell in rows:
                cell.font = text_font_data
                cell.alignment = align_left
                cell.border = border
    for x in range(6,ws.max_row + 1):
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=1, max_col=2):
            for cell in rows:
                cell.font = text_font_data
                cell.alignment = align_center
                cell.border = border
    # for x in range(61,64):
    for rows in ws.iter_rows(min_row=4, max_row=5, min_col=1, max_col=65):
        for cell in rows:
            cell.fill = PatternFill(fgColor="f4f087", fill_type = "solid")
    for rows in ws.iter_rows(min_row=6, max_row=ws.max_row - 1, min_col=15, max_col=15):
        for cell in rows:
            cell.fill = PatternFill(fgColor="FABF8F", fill_type = "solid")
    # for x in range(26,34):
    for rows in ws.iter_rows(min_row=6, max_row=ws.max_row - 1, min_col=26, max_col=34):
        for cell in rows:
            cell.fill = PatternFill(fgColor="FABF8F", fill_type = "solid")
    for rows in ws.iter_rows(min_row=6, max_row=ws.max_row - 1, min_col=46, max_col=51):
        for cell in rows:
            cell.fill = PatternFill(fgColor="FABF8F", fill_type = "solid")
    for rows in ws.iter_rows(min_row=6, max_row=ws.max_row - 1, min_col=53, max_col=53):
        for cell in rows:
            cell.fill = PatternFill(fgColor="FABF8F", fill_type = "solid")
    for rows in ws.iter_rows(min_row=6, max_row=ws.max_row - 1, min_col=62, max_col=62):
        for cell in rows:
            cell.fill = PatternFill(fgColor="FABF8F", fill_type = "solid")
    for rows in ws.iter_rows(min_row=ws.max_row , max_row=ws.max_row , min_col=1, max_col=65):
        for cell in rows:
            cell.fill = PatternFill(fgColor="f4f087", fill_type = "solid")
            cell.border = border
    

def set_column_widths(ws):
    column_widths = [10] *2 + [20] *1 + [10] * 3 + [20] * 2 + [10]*55
    # column_widths = [6, 5] + [5] * 13 + [7] * 2 + [5] * 1 +[6] * 1 + [5] * 4 +[6] * 1 + [4] * 5+ [8] * 7
    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
    row_heights = [60, 60, 20,20,40] + [20] * (ws.max_row - 1) +[30]*1 # Example row heights
    for i, height in enumerate(row_heights, start=1):
        ws.row_dimensions[i].height = height

def build_xlsx_response(filename):
    xlsx_file = make_xlsx(sheet_name=filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'

def get_leave_count(employee, leave_type, from_date, to_date):
    if not leave_type:
        frappe.throw("Leave Type is required.")

    # Ensure date format consistency (use getdate if necessary)
    from_date = getdate(from_date)
    to_date = getdate(to_date)
    full_day_leave_count = halfdays_leave_count = leave_count = 0
    full_day_leave_count = frappe.db.count("Attendance", {
        'employee': employee,
        'leave_type': leave_type,
        'status': 'On Leave',
        'attendance_date': ['between', [from_date, to_date]],
        'docstatus':["!=",2],
    })
    halfdays_leave_count = frappe.db.count("Attendance", {
        'employee': employee,
        'leave_type': leave_type,
        'status': 'Half Day',
        'attendance_date': ['between', [from_date, to_date]],
        'docstatus':["!=",2],
    })
    leave_count = full_day_leave_count + (halfdays_leave_count / 2)
    return leave_count


def get_holiday_count(employee, from_date, to_date):
    holiday_list = frappe.db.get_value('Employee', employee, 'holiday_list')
    total_weekoff = 0
    total_public_holiday = 0
    total_other_holiday = 0

    if holiday_list:
        holiday_records = frappe.db.sql("""
            SELECT holiday_date, weekly_off, holiday_type
            FROM `tabHoliday`
            WHERE parent = %s AND holiday_date BETWEEN %s AND %s
        """, (holiday_list, from_date, to_date), as_dict=True)

        for record in holiday_records:
            if record['weekly_off'] == 1:
                total_weekoff += 1
            elif record['holiday_type'] == "PH":
                total_public_holiday += 1
            else:
                total_other_holiday += 1

    return {
        'total_weekoff': total_weekoff,
        'total_public_holiday': total_public_holiday,
        'total_other_holiday': total_other_holiday,
        'total_holiday': total_weekoff + total_public_holiday
    }
      

def get_data(args):
    from_date = args.get('from_date')
    to_date = args.get('to_date')

    if not from_date or not to_date:
        frappe.throw("From Date and To Date are required.")
    total_working_days = emp_basic = total_cl_count = absent_total = 0
    emp_house_rent_allowance = emp_conveyance_allowance = emp_education_allowance = emp_food_allowance = emp_attire_allowance = emp_special_allowance = 0
    emp_medical_allowance = emp_mobile_allowance = present_days_count = emp_fixed_earning = holidays_count = total_el_count = total_coff_count = 0
    total_sl_count = other_holiday_count = total_lop_count = payment_days = basic = conveyance = hra = gross_pay = education_allowance = 0
    food_allowance = attire_allowance = mobile_allowance = medical_allowance = special_allowance = total_el_amount = attendance_allowance = total_earnings_amount = 0
    total_deduction = net_pay = loan = others = pf = pt = lwf = esi = other_allowances = overtime =travel_llowance = bonus = heat_allowance = 0
    from_date_str =from_date

    if isinstance(from_date_str, str):
        month_year_format_str = datetime.strptime(from_date_str, '%Y-%m-%d')
    else:
        month_year_format_str = from_date_str  

    month_year_format = month_year_format_str.strftime('%B %Y')
    data = [
            [""],

            ["SALARY STATEMENT FOR THE MONTH OF " + month_year_format + " - STAFF"],

            ["S.No", "Emp Code", "Name", "DOB", "Grade", "DOJ", "Department", "Designation", "Bank A/C No", 
             "Mode", "UAN No.", "ESIC No.", "PAN No", "Category", "No Working day", "Fixed Gross"] + 
            [""] * 9 + ["Present Days", "S/PH", "COFF", "CL", "SL", "EL", "N/F", "LOP", "Absent", "NPD", 
             "GROSS EARNINGS"] + [""] * 12 + ["VARIABLE EARNINGS"] + [""] * 5 + 
            ["Total Earnings", "Deductions"] + [""] * 7 + ["Total Deductions", "Net Pay INR"],

            [""] * 15 + 
            ["Basic", "HRA", "Conveyance", "Education", "Food Allow", "Attire Allowance", 
             "Mobile Allowance", "Medical Reimbursement", "Spl Allow", "Total Fixed Gross Earning"] + 
            [""] * 10 + ["Basic", "HRA", "Conveyance", "Education", "Food Allow", "Attire Allowance", 
             "Mobile Allowance", "Medical Reimbursement", "Spl Allow", "Total Gross Earning", 
             "EL Encashment", "Gratuity Pay", "Attendance Bonus", "Heat Allowance","Travel Allowance", "Bonus", "OT Hrs", 
             "OT Amount", "Other Allowance","", "EPF Round Off", "ESIC Round up off","LWF","PT", 
             "Canteen", "Other Deduction", "Loan", "TDS Deduction"]
        ]

    salary_slips = frappe.db.sql("""
    SELECT * 
    FROM `tabSalary Slip`
    WHERE start_date = %s AND end_date = %s AND docstatus != 2 AND salary_structure = 'Staff'
""", (from_date, to_date), as_dict=True)


    index = 0
    for s in salary_slips:
        if not isinstance(s, dict):
            continue  

        index += 1
        present_days_count = 0
        halfdays_count = 0

        emp_data = frappe.get_list(
            'Employee',
            filters={'name': s['employee']},
            fields=["date_of_birth", 'date_of_joining', 'bank_ac_no', 'salary_mode', 'pan_number', 'employee_category',
            'basic','house_rent_allowance','conveyance_allowance','education_allowance','food_allowance','attire_allowance',
            'mobile_allowance','medical_allowance','special_allowance','fixed_earning','esic_no'
            ],
            limit_page_length=1
        )

        emp = emp_data[0] if emp_data else frappe._dict({
            "date_of_birth": None,
            "date_of_joining": None,
            "bank_ac_no": None,
            "salary_mode": None,
            "pan_number": None,
            "employee_category": None,
            "basic":None,
            "house_rent_allowance":None,
            "conveyance_allowance":None,
            "education_allowance":None,
            "food_allowance":None,
            "attire_allowance":None,
            "mobile_allowance":None,
            "medical_allowance":None,
            "special_allowance":None,
            "fixed_earning":None,
            'esic_no':None,
        })
        holiday_data = get_holiday_count(s['employee'], from_date, to_date)
        present_days_count = frappe.db.count(
            "Attendance", 
            filters={
                'employee': s['employee'],
                'status': 'Present',  
                'attendance_date': ['between', [from_date, to_date]],
                'docstatus':["!=",2],  
            }
        )
        halfdays_count = frappe.db.count(
            "Attendance", 
            filters={
                'employee': s['employee'],
                'status': 'Half Day',  
                'attendance_date': ['between', [from_date, to_date]],
                'docstatus':["!=",2], 
            }
        )
        present_days = present_days_count + (halfdays_count / 2)

        
        
        coff_count = get_leave_count(s['employee'], "Compensatory Off", from_date, to_date)
        sl_count = get_leave_count(s['employee'], "Sick Leave", from_date, to_date)
        el_count = get_leave_count(s['employee'], "Earned Leave", from_date, to_date)
        cl_count = get_leave_count(s['employee'], "Casual Leave", from_date, to_date)
        lop_count = get_leave_count(s['employee'], "Leave Without Pay", from_date, to_date)

        # Fetch salary components
        components = ['Basic', 'House Rent Allowance', 'Conveyance', 'Education Allowance',
            'Food Allowance', 'Medical Reimbursement', 'Special Allowance',
            'Attire Allowance', 'Mobile Allowance', 'Heat Allowance', 'Other Allowances',
            'Overtime', 'Attendance Allowance', 'Travel Allowance','Bonus', 'Provident Fund',
            'Employer State Insurance', 'Professional Tax', 'Loan', 'Others','Labour Welfare Fund']

        # Fetch salary components for the given salary slip
        el_amount = frappe.get_value("Salary Detail", {'parent': s['name'], 'salary_component': 'EL Encashment'}, 'amount') or 0.0
        salary_details = {}
        for comp in components:
            salary_amount = frappe.get_value("Salary Detail", {'parent': s['name'], 'salary_component': comp}, 'amount') or 0.0
            salary_details[comp] = salary_amount

        total_earnings = (
            s['gross_pay'] + salary_details['Attendance Allowance'] +
            salary_details['Heat Allowance'] + salary_details['Travel Allowance'] + salary_details['Bonus'] + 
            salary_details['Overtime'] + salary_details['Other Allowances'] + el_amount
        )

        fromdate = datetime.strptime(str(s['date_of_joining']), '%Y-%m-%d')
        dob = fromdate.strftime('%d-%m-%Y')
        fromdate = datetime.strptime(str(s['date_of_birth']), '%Y-%m-%d')
        doj = fromdate.strftime('%d-%m-%Y')
        row = [
            index, s['employee'], s['employee_name'], dob, s['grade'], doj, s['department'],
            s['designation'], emp.bank_ac_no, emp.salary_mode, s['uan_no'], emp.esic_no, emp.pan_number, emp.employee_category,
            s['total_working_days'], emp.basic or 0, emp.house_rent_allowance or 0, emp.conveyance_allowance or 0,
            emp.education_allowance or 0, emp.food_allowance or 0, emp.attire_allowance or 0, emp.mobile_allowance or 0,
            emp.medical_allowance or 0, emp.special_allowance or 0, emp.fixed_earning or 0, present_days, holiday_data['total_holiday'],
            coff_count, cl_count, sl_count, el_count, holiday_data['total_other_holiday'], lop_count, s['absent_days'], s['payment_days'],
            salary_details['Basic'],
            salary_details['House Rent Allowance'], salary_details['Conveyance'], salary_details['Education Allowance'],
            salary_details['Food Allowance'], salary_details['Attire Allowance'], salary_details['Mobile Allowance'],
            salary_details['Medical Reimbursement'], salary_details['Special Allowance'], s['gross_pay'],el_amount, 0,
            salary_details['Attendance Allowance'], salary_details['Heat Allowance'], salary_details['Travel Allowance'], salary_details['Bonus'] ,0,
            salary_details['Overtime'], salary_details['Other Allowances'], total_earnings, salary_details['Provident Fund'],
            salary_details['Employer State Insurance'],salary_details['Labour Welfare Fund'], salary_details['Professional Tax'], 0,
            salary_details['Others'],
            salary_details['Loan'],0, s['total_deduction'], s['net_pay']
        ]
        data.append(row)
        total_working_days += s['total_working_days']
        emp_basic += emp.basic
        emp_house_rent_allowance += emp.house_rent_allowance
        emp_conveyance_allowance += emp.conveyance_allowance
        emp_education_allowance +=  emp.education_allowance
        emp_food_allowance += emp.food_allowance
        emp_attire_allowance += emp.attire_allowance
        emp_mobile_allowance += emp.mobile_allowance 
        emp_medical_allowance += emp.medical_allowance
        emp_special_allowance += emp.special_allowance
        emp_fixed_earning += emp.fixed_earning
        present_days_count += present_days
        holidays_count += int(holiday_data['total_holiday'])
        total_coff_count += coff_count
        total_cl_count += cl_count
        total_sl_count += sl_count
        total_el_count += el_count
        other_holiday_count += holiday_data['total_other_holiday']
        total_lop_count += lop_count
        absent_total += s['absent_days']
        payment_days += s['payment_days']
        basic += salary_details['Basic']
        hra += salary_details['House Rent Allowance']
        conveyance += salary_details['Conveyance']
        education_allowance += salary_details['Education Allowance']
        food_allowance += salary_details['Food Allowance']
        attire_allowance += salary_details['Attire Allowance']
        mobile_allowance += salary_details['Mobile Allowance']
        medical_allowance += salary_details['Medical Reimbursement']
        special_allowance += salary_details['Special Allowance']
        gross_pay += s['gross_pay']
        total_el_amount += el_amount
        total_earnings_amount += total_earnings
        attendance_allowance += salary_details['Attendance Allowance']
        heat_allowance += salary_details['Heat Allowance']
        travel_llowance += salary_details['Travel Allowance']
        bonus += salary_details['Bonus']
        overtime += salary_details['Overtime']
        other_allowances += salary_details['Other Allowances']
        pf += salary_details['Provident Fund']
        esi += salary_details['Employer State Insurance']
        lwf += salary_details['Labour Welfare Fund']
        pt += salary_details['Professional Tax']
        others += salary_details['Others']
        loan += salary_details['Loan']
        total_deduction += s['total_deduction']
        net_pay += s['net_pay']
    data.append([""]*14 +[total_working_days,emp_basic,emp_house_rent_allowance,emp_conveyance_allowance,emp_education_allowance,emp_food_allowance,emp_attire_allowance,
    emp_mobile_allowance,emp_medical_allowance,emp_special_allowance,emp_fixed_earning,present_days_count,holidays_count,
    total_coff_count,total_cl_count,total_sl_count,total_el_count,other_holiday_count,total_lop_count,absent_total,payment_days,basic,hra,conveyance,education_allowance,
    food_allowance,attire_allowance,mobile_allowance,medical_allowance,special_allowance,gross_pay,total_el_amount,0,attendance_allowance,heat_allowance,
    travel_llowance,bonus,0,overtime,other_allowances,total_earnings_amount,pf,esi,lwf,pt,0,others,loan,0,total_deduction,net_pay])
    return data