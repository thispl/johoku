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
    filename = 'Salary Summary.xlsx'
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
    # image_data = requests.get(image_url).content
    image_data = requests.get(image_url, verify=False).content
    img = xlImage(io.BytesIO(image_data))
    img_cell = ws.cell(row=1, column=6)
    img.width = 100
    img.height = 80
    ws.add_image(img,"H1")
         
        
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=9)
    ws["J1"].value = "JOHOKU MANUFACTURING PRIVATE LIMITED"
    ws["J1"].alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    ws["J1"].font = Font(bold=True, size=14)
    ws.merge_cells(start_row=1, start_column=10, end_row=1, end_column=17)
    for row in data:
        if not isinstance(row, (list, tuple)):
            row = [row]  
        ws.append(row)

    
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=17)
    for x in range(1,12):
        ws.merge_cells(start_row=3, start_column=x, end_row=5, end_column=x)
    ws.merge_cells(start_row=3, start_column=12, end_row=3, end_column=15)
    for x in range(12,16):
        ws.merge_cells(start_row=4, start_column=x, end_row=5, end_column=x)
    ws.merge_cells(start_row=3, start_column=16, end_row=5, end_column=16)
    ws.merge_cells(start_row=3, start_column=17, end_row=5, end_column=17)
    ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=2)
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
    text_font_header_data = Font(bold=True, size=9)
    text_font_data = Font(bold=False, size=9)
    thin_border = Side(border_style="thin", color="000000")
    border = Border(
        left=Side(border_style='thin'),
        right=Side(border_style='thin'),
        top=Side(border_style='thin'),
        bottom=Side(border_style='thin')
    )
    outline_border = Border(
    left=thin_border,
    right=thin_border,
    top=thin_border,
    bottom=thin_border
)
    outline_border_new = Border(
    left=thin_border,
    top=thin_border,
)

# Apply the outline border for the entire range
    outline_range = ws.iter_rows(min_row=1, max_row=1, min_col=17, max_col=17)
    for rows in outline_range:
        for cell in rows:
            cell.border = outline_border_new
    outline_range = ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=17)
    for rows in outline_range:
        for cell in rows:
            cell.border = outline_border
    for rows in ws.iter_rows(min_row=2, max_row=2, min_col=1, max_col=17):
        for cell in rows:
            cell.font = header_font
            cell.alignment = align_center
            cell.border = border
    for x in range(3,6):
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=1, max_col=17):
            for cell in rows:
                cell.font = text_font_header
                cell.alignment = align_center
                cell.border = border
    for x in range(6,ws.max_row + 1):
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=2, max_col=2):
            for cell in rows:
                cell.font = text_font_data
                cell.alignment = align_center
                cell.border = border
    for x in range(6,ws.max_row + 1):
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=1, max_col=1):
            for cell in rows:
                cell.font = text_font_header_data
                cell.alignment = align_center
                cell.border = border
    for x in range(6,ws.max_row + 1):
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=3, max_col=17):
            for cell in rows:
                cell.font = text_font_data
                cell.alignment = align_right
                cell.border = border
    for rows in ws.iter_rows(min_row=3, max_row=5, min_col=1, max_col=17):
        for cell in rows:
            cell.fill = PatternFill(fgColor="f4f087", fill_type = "solid")
    
    

def set_column_widths(ws):
    column_widths = [11] *20
    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
    row_heights = [60, 60, 30,30,30] + [20] * (ws.max_row - 1) +[30]*1 
    for i, height in enumerate(row_heights, start=1):
        ws.row_dimensions[i].height = height

def build_xlsx_response(filename):
    xlsx_file = make_xlsx(sheet_name=filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'

def get_salary_component_data(slip_name_list):
    basic_amount = ot_amount = attendance_amount = heat_allowance_amount = tl_llowance_amount = el_amount = other_allowances_amount = pf_amount = 0
    esic_amount = pt_amount = loan_amount = others_amount = total_earnings_amount  = 0
    gratuity_amount = bonus_amount = tds_deduction_amount = 0
    lwf_amount = 0
    arear_amount =0
    tds_amount =0
    hra_amount = conveyance_amount = education_allowance_amount = food_allowance_amount = attire_allowance_amount = mobile_allowance_amount = medical_allowance_amount = special_allowance_amount = 0
    components = ['Basic', 'Overtime', 'Attendance Allowance', 'Heat Allowance','TL Allowance','EL Encashment','Arear Allowance',
        'Provident Fund','Employer State Insurance', 'Professional Tax', 'Loan', 'Others',"House Rent Allowance","Conveyance","Education Allowance","Food Allowance",
        "Attire Allowance","Mobile Allowance","Medical Re imbursement","Special Allowance","Labour Welfare Fund","TDS Deduction"]
    for slip_name in slip_name_list:
        for comp in components:
            if comp == "Basic":
                basic = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                basic_amount += basic[0]['salary_amt'] or 0
            elif comp == "Overtime":
                ot = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                ot_amount += ot[0]['salary_amt'] or 0
            elif comp == "Attendance Allowance":
                attendance = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                attendance_amount += attendance[0]['salary_amt'] or 0
            elif comp == "Heat Allowance":
                heat_allowance = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                heat_allowance_amount += heat_allowance[0]['salary_amt'] or 0
            elif comp == "TL Allowance":
                tl_llowance = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                tl_llowance_amount += tl_llowance[0]['salary_amt'] or 0
            elif comp == "EL Encashment":
                el = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                el_amount += el[0]['salary_amt'] or 0
            elif comp == "Arear Allowance":
                other_allowances = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                other_allowances_amount += other_allowances[0]['salary_amt'] or 0
            elif comp == "Provident Fund":
                pf = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                pf_amount += pf[0]['salary_amt'] or 0
            elif comp == "Employer State Insurance":
                esic = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                esic_amount += esic[0]['salary_amt'] or 0
            elif comp == "Professional Tax":
                pt = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                pt_amount += pt[0]['salary_amt'] or 0
            elif comp == "Loan":
                loan = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                loan_amount += loan[0]['salary_amt'] or 0
            elif comp == "Others":
                others = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                others_amount += others[0]['salary_amt'] or 0
            elif comp == "House Rent Allowance":
                hra = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                hra_amount += hra[0]['salary_amt'] or 0
            elif comp == "Conveyance":
                conveyance = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                conveyance_amount += conveyance[0]['salary_amt'] or 0
            elif comp == "Education Allowance":
                education_allowance = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                education_allowance_amount += education_allowance[0]['salary_amt'] or 0
            elif comp == "Food Allowance":
                food_allowance = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                food_allowance_amount += food_allowance[0]['salary_amt'] or 0
            elif comp == "Attire Allowance":
                attire_allowance = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                attire_allowance_amount += attire_allowance[0]['salary_amt'] or 0
            elif comp == "Mobile Allowance":
                mobile_allowance = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                mobile_allowance_amount += mobile_allowance[0]['salary_amt'] or 0
            elif comp == "Medical Re imbursement":
                medical_allowance = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                medical_allowance_amount += medical_allowance[0]['salary_amt'] or 0
            elif comp == "Special Allowance":
                special_allowance = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                special_allowance_amount += special_allowance[0]['salary_amt'] or 0
            elif comp == "Labour Welfare Fund":
                lwf = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                print(lwf)
                lwf_amount += lwf[0]['salary_amt'] or 0
            elif comp == "Gratuity":
                gratuity = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                gratuity_amount += gratuity[0]['salary_amt'] or 0
            elif comp == "Bonus":
                bonus = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                bonus_amount += bonus[0]['salary_amt'] or 0
            elif comp == "TDS Deduction":
                tds_deduction = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                tds_deduction_amount += tds_deduction[0]['salary_amt'] or 0
            elif comp =="Arear Allowance":
                arear = frappe.db.sql(""" SELECT SUM(amount) AS salary_amt FROM `tabSalary Detail` WHERE parent = %s AND salary_component = %s """, (slip_name, comp), as_dict=True)
                arear_amount += arear[0]['salary_amt'] or 0

            total_earnings_amount = basic_amount + hra_amount+conveyance_amount+education_allowance_amount+food_allowance_amount+attire_allowance_amount+mobile_allowance_amount+medical_allowance_amount+special_allowance_amount
    data = [basic_amount,ot_amount,attendance_amount,heat_allowance_amount,tl_llowance_amount,el_amount,other_allowances_amount,pf_amount,
    esic_amount,pt_amount,loan_amount,others_amount,total_earnings_amount,lwf_amount,gratuity_amount, bonus_amount,tds_deduction_amount,arear_amount]
    
    return data

def get_data(args):
# def get_data():
#     from_date ="2024-11-21"
#     to_date ="2024-12-20"
    from_date = args.get('from_date')
    to_date = args.get('to_date')

    if not from_date or not to_date:
        frappe.throw("From Date and To Date are required.")
    to_date_str =to_date

    if isinstance(to_date_str, str):
        month_year_format_str = datetime.strptime(to_date_str, '%Y-%m-%d')
    else:
        month_year_format_str = to_date_str  

    month_year_format = month_year_format_str.strftime('%B %Y')
    data = [
            ["SALARY STATEMENT FOR THE MONTH OF " + month_year_format.upper()],
            ["S.No","Category","Count","Earned Basic","Total Earned Gross","TL Allowance","Attendance Allowance","Heat Allowance",
            "Overtime Amount","Arear Allowance","Total Earning","Deductions","","","","Total Deduction","Net Salary"],
            [""]*11 + ["EPF Round Off","ESIC Round Off","Prof Tax","Loan"],
            [""]
        ]
    categories = ['Staff', 'DT', 'ITI', 'GT', 'TT']
    total_basic = total_employee_count = 0
    total_gross_salary = total_ot = total_att = total_heat = total_tl = total_el = total_other_allow = total_pf = total_esi = total_pt = total_loan =0
    total_others = total_deduction_salary = total_gross_salary = total_net_pay_salary = total_sum_of_gross_pay = total_earnings_amount_overall =0.0
    total_other_and_arear_allow =0
    total_arear_allowance=0
    row =[]
    index = total_lwf = 0
    total_gratuity = total_bonus =total_tds = 0
    for category in categories:
        index += 1
        if category == 'Staff':
            employee_category = "Staff"
        elif category == 'DT':
            employee_category = "DT Trainee"
        elif category == 'ITI':
            employee_category = "ITI Trainee"
        elif category == 'GT':
            employee_category = "GT Trainee"
        elif category == 'TT':
            employee_category = "TT Trainee"
        slip_name_list = []
        salary_slips = frappe.db.sql(""" SELECT * FROM `tabSalary Slip` WHERE start_date = %s AND end_date = %s AND docstatus != 2 AND employee_category = %s""", (from_date, to_date, category), as_dict=True)
        salary_slip_data = frappe.db.sql(""" SELECT COUNT(employee) AS employee_count, SUM(gross_pay) AS sum_of_gross_pay,SUM(total_deduction) AS total_deduction,SUM(net_pay) AS total_net_pay FROM `tabSalary Slip` WHERE start_date = %s AND end_date = %s AND docstatus != 2 AND employee_category = %s""", (from_date, to_date,category), as_dict=True)

        employee_count = salary_slip_data[0].employee_count or 0
        sum_of_gross_pay = salary_slip_data[0].sum_of_gross_pay or 0.0
        total_deduction = salary_slip_data[0].total_deduction or 0.0
        total_net_pay = salary_slip_data[0].total_net_pay or 0.0
        total_gross = 0
        for s in salary_slips:
            if not isinstance(s, dict):
                continue  
            slip_name_list.append(s['name'])
            employee_data = frappe.db.sql(""" SELECT fixed_earning FROM `tabEmployee` WHERE name = %s""", (s['employee']), as_dict=True)
            fixed_earning = employee_data[0].fixed_earning
            total_gross += fixed_earning
        # print(slip_name_list)
        staff_data = get_salary_component_data(slip_name_list)
        # print(staff_data)
        # print(sum_of_gross_pay)    
        # print(employee_category)
        total_employee_count += employee_count
        total_basic += int(staff_data[0])
        total_gross_salary += total_gross
        total_ot += int(staff_data[1])
        total_att += int(staff_data[2])
        total_heat += int(staff_data[3])
        total_tl += int(staff_data[4])
        # total_el += int(staff_data[5])
        total_other_allow += int(staff_data[6])
        total_pf += int(staff_data[7])
        total_esi += int(staff_data[8])
        total_pt += int(staff_data[9])
        total_loan += int(staff_data[10])
        total_others += int(staff_data[11])
        total_earnings_amount_overall += int(staff_data[12])
        total_lwf += int(staff_data[13])
        # frappe.log_error(str(staff_data[13]), "Staff Data Debug")
        print(total_lwf)
        # total_gratuity += int(staff_data[14])
        # total_bonus += int(staff_data[15])
        total_tds += int(staff_data[16])
        total_arear_allowance += int(staff_data[17])
        total_deduction_salary += int(total_deduction)
        total_net_pay_salary += int(total_net_pay)
        total_sum_of_gross_pay += int(sum_of_gross_pay)
        total_deduction_int = int(total_deduction)
        formatted_number = format_currency(total_deduction_int)
        other_and_arear_allow = int(staff_data[6]) + int(staff_data[17])
        total_other_and_arear_allow +=other_and_arear_allow
        row =[
            index,
            employee_category,  
            int(employee_count),
            int(staff_data[0]),#sno
            int(staff_data[12]),#c
            int(staff_data[4]),#b
            int(staff_data[2]),#e
            int(staff_data[3]),
            # int(staff_data[5]),#el
            # int(staff_data[15]),#b
            # int(staff_data[14]),#g
            int(staff_data[1]),
            # int(staff_data[6]),
            int(other_and_arear_allow),
            int(sum_of_gross_pay), 
            int(staff_data[7]),
            int(staff_data[8]), 
            int(staff_data[9]),
            int(staff_data[10]),
            # int(staff_data[16]),#tds
            # int(staff_data[13]),
            # int(staff_data[11]),
            formatted_number,
            int(total_net_pay)]
        data.append(row)
        # print (row)
    # print(total_basic)
    total_deduction_salary_int = int(total_deduction_salary)
    formatted_number_total = format_currency(total_deduction_salary_int)
    list_of_total = ["Total","",int(total_employee_count),int(total_basic),
    int(total_earnings_amount_overall), int(total_tl), int(total_att), int(total_heat), int(total_ot), int(total_other_and_arear_allow),int(total_sum_of_gross_pay), int(total_pf),
    int(total_esi), int(total_pt), int(total_loan), formatted_number_total, int(total_net_pay_salary)
]     
    data.append(list_of_total)
    return data

def format_currency(value):
    if value is None:
        return "0"
    
    number_str = str(int(value))
    
    if len(number_str) > 3:
        last_three = number_str[-3:]  
        other_digits = number_str[:-3] 
        
        formatted_other = []
        while len(other_digits) > 2:
            formatted_other.append(other_digits[-2:])
            other_digits = other_digits[:-2]
        if other_digits:
            formatted_other.append(other_digits)        
        formatted_other.reverse()
        formatted_number = ','.join(formatted_other) + ',' + last_three
    else:
        formatted_number = number_str
    
    return formatted_number