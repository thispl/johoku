# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from six import BytesIO
from datetime import datetime
from datetime import datetime, timedelta
from frappe.utils import (getdate, cint, add_months, date_diff, add_days, format_date,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
import pandas as pd
class ManPowerCategoryWisePlanVsActualSummary(Document):
    pass



@frappe.whitelist()
def download():
    filename = 'ManPowerCategoryWisePlanVsActualSummary.xlsx'
    build_xlsx_response(filename)

def make_xlsx(sheet_name=None):
    args = frappe.local.form_dict
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name if sheet_name else 'Sheet1'
    frappe.errprint(args)
    data = get_data(args)
    if not data:  # Check if data is empty or None
        frappe.throw("No data available to generate the report.")
    
    for row in data:
        if not isinstance(row, (list, tuple)):
            row = [row]  # Convert to a list if it's a single item (likely a string)
        ws.append(row)

    # Merging cells based on the number of rows in the header
    ws.merge_cells(start_row=3, start_column=1, end_row=4, end_column=1)
    ws.merge_cells(start_row=1, start_column=1, end_row=2, end_column=32)
    ws.merge_cells(start_row=3, start_column=2, end_row=4, end_column=18)
    ws.merge_cells(start_row=3, start_column=19, end_row=4, end_column=28)
    ws.merge_cells(start_row=3, start_column=29, end_row=4, end_column=32)
    ws.merge_cells(start_row=5, start_column=1, end_row=9, end_column=1)
    ws.merge_cells(start_row=5, start_column=18, end_row=9, end_column=18)
    ws.merge_cells(start_row=5, start_column=2, end_row=7, end_column=3)
    ws.merge_cells(start_row=5, start_column=4, end_row=7, end_column=5)
    ws.merge_cells(start_row=5, start_column=6, end_row=7, end_column=7)
    ws.merge_cells(start_row=5, start_column=8, end_row=7, end_column=9)
    ws.merge_cells(start_row=5, start_column=10, end_row=7, end_column=11)
    ws.merge_cells(start_row=5, start_column=12, end_row=7, end_column=13)
    ws.merge_cells(start_row=5, start_column=14, end_row=7, end_column=15)
    ws.merge_cells(start_row=5, start_column=16, end_row=7, end_column=17)
    ws.merge_cells(start_row=8, start_column=2, end_row=9, end_column=2)
    ws.merge_cells(start_row=8, start_column=3, end_row=9, end_column=3)
    ws.merge_cells(start_row=8, start_column=4, end_row=9, end_column=4)
    ws.merge_cells(start_row=8, start_column=5, end_row=9, end_column=5)
    ws.merge_cells(start_row=8, start_column=6, end_row=9, end_column=6)
    ws.merge_cells(start_row=8, start_column=7, end_row=9, end_column=7)
    ws.merge_cells(start_row=8, start_column=8, end_row=9, end_column=8)
    ws.merge_cells(start_row=8, start_column=9, end_row=9, end_column=9)
    ws.merge_cells(start_row=8, start_column=10, end_row =9, end_column=10)
    ws.merge_cells(start_row=8, start_column=11, end_row =9, end_column=11)
    ws.merge_cells(start_row=8, start_column=12, end_row =9, end_column=12)
    ws.merge_cells(start_row=8, start_column=13, end_row =9, end_column=13)
    ws.merge_cells(start_row=8, start_column=14, end_row =9, end_column=14)
    ws.merge_cells(start_row=8, start_column=15, end_row =9, end_column=15)
    ws.merge_cells(start_row=8, start_column=16, end_row =9, end_column=16)
    ws.merge_cells(start_row=8, start_column=17, end_row =9, end_column=17)
    ws.merge_cells(start_row=5, start_column=19, end_row=7, end_column=22)
    ws.merge_cells(start_row=5, start_column=23, end_row=9, end_column=23)
    ws.merge_cells(start_row=5, start_column=24, end_row=9, end_column=24)
    ws.merge_cells(start_row=5, start_column=25, end_row=9, end_column=26)
    ws.merge_cells(start_row=5, start_column=27, end_row=9, end_column=28)
    ws.merge_cells(start_row=5, start_column=29, end_row=9, end_column=29)
    ws.merge_cells(start_row=5, start_column=30, end_row=9, end_column=30)
    ws.merge_cells(start_row=5, start_column=31, end_row=9, end_column=31)
    ws.merge_cells(start_row=5, start_column=32, end_row=9, end_column=32)
    # ws.merge_cells(start_row=7, start_column=19, end_row=8, end_column=19)
    ws.merge_cells(start_row=8, start_column=19, end_row=8, end_column=22)
    for x in range(10,ws.max_row+1):
        ws.merge_cells(start_row=x, start_column=25, end_row=x, end_column=26)
        ws.merge_cells(start_row=x, start_column=27, end_row=x, end_column=28)

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
    text_font_header = Font(bold=True, size=12)
    text_font_data = Font(bold=False, size=9)
    border = Border(
        left=Side(border_style='thin'),
        right=Side(border_style='thin'),
        top=Side(border_style='thin'),
        bottom=Side(border_style='thin')
    )
    
    for rows in ws.iter_rows(min_row=1, max_row=2, min_col=1, max_col=32):
        for cell in rows:
            cell.font = header_font
            cell.alignment = align_center
            cell.border = border

    for rows in ws.iter_rows(min_row=3, max_row=4, min_col=2, max_col=18):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=3, max_row=4, min_col=1, max_col=2):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=3, max_row=4, min_col=19, max_col=28):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=3, max_row=4, min_col=29, max_col=32):
        for cell in rows:
            cell.font = text_font_header
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=1, max_col=2):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=2, max_col=3):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=4, max_col=5):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=6, max_col=7):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=8, max_col=9):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=10, max_col=11):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=12, max_col=13):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=14, max_col=15):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=16, max_col=17):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=18, max_col=18):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for x in range(2,19):
        for rows in ws.iter_rows(min_row=8, max_row=9, min_col=x, max_col=x):
            for cell in rows:
                cell.font = text_font
                cell.alignment = align_center
                cell.border = border
    
    for rows in ws.iter_rows(min_row=8, max_row=9, min_col=20, max_col=20):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=8, max_row=9, min_col=22, max_col=22):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=23, max_col=23):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=8, max_row=7, min_col=19, max_col=22):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=8, max_row=9, min_col=21, max_col=21):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=8, max_row=9, min_col=22, max_col=22):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=24, max_col=24):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=25, max_col=25):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=26, max_col=26):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=27, max_col=29):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for x in range(30,33):
        for rows in ws.iter_rows(min_row=5, max_row=7, min_col=x, max_col=x):
            for cell in rows:
                cell.font = text_font
                cell.alignment = align_center
                cell.border = border
    for rows in ws.iter_rows(min_row=5, max_row=7, min_col=19, max_col=23):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    # for rows in ws.iter_rows(min_row=8, max_row=7, min_col=20, max_col=21):
    #     for cell in rows:
    #         cell.font = text_font
    #         cell.alignment = align_center
    #         cell.border = border
    for rows in ws.iter_rows(min_row=8, max_row=9, min_col=19, max_col=19):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=3, max_row=4, min_col=1, max_col=1):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for rows in ws.iter_rows(min_row=8, max_row=9, min_col=1, max_col=1):
        for cell in rows:
            cell.font = text_font
            cell.alignment = align_center
            cell.border = border
    for x in range (10,ws.max_row+1):
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=27, max_col=28):
            for cell in rows:
                cell.font = text_font_data
                cell.alignment = align_right
                cell.border = border
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=25, max_col=26):
            for cell in rows:
                cell.font = text_font_data
                cell.alignment = align_right
                cell.border = border
    for x in range (10,ws.max_row+1):
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=1, max_col=1):
            for cell in rows:
                cell.font = text_font
                cell.alignment = align_left
                cell.border = border
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=2, max_col=24):
            for cell in rows:
                cell.font = text_font_data
                cell.alignment = align_right
                cell.border = border
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=29, max_col=32):
            for cell in rows:
                cell.font = text_font_data
                cell.alignment = align_right
                cell.border = border
        for rows in ws.iter_rows(min_row=8, max_row=9, min_col=23, max_col=32):
            for cell in rows:
                cell.font = text_font
                cell.alignment = align_center
                cell.border = border
def set_column_widths(ws):
    column_widths = [18, 5] + [5] * 13 + [7] * 2 + [5] * 1 +[6] * 1 + [5] * 4 +[6] * 1 + [4] * 5+ [8] * 7
    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
    ws.column_dimensions[openpyxl.utils.get_column_letter(32)].width = 80
def build_xlsx_response(filename):
    xlsx_file = make_xlsx(sheet_name=filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'


def get_data(args):
    # frappe.errprint(args)
    if args.get('start_date') and args.get('end_date'):
          # Default to [1, 2] if not provided
        start_date =args.get('start_date')
        end_date =args.get('end_date')
        # frappe.errprint(end_date)
        # frappe.errprint(start_date)
        fromdate = datetime.strptime(args.get('start_date'), '%Y-%m-%d').date()
        fromdate_ = fromdate.strftime('%d-%m-%Y')
        todate = datetime.strptime(args.get('end_date'), '%Y-%m-%d').date()
        todate_ = todate.strftime('%d-%m-%Y')
        if not args.get('shift'):
            shift_header = 'All Shift'
        else:
            shift_header = args.get('shift')
        data = [
            ["Manpower Category wise plan vs Actual Summary"],
            [""],
            ["", "Plan / Actual"] + [""] * 16 + ["Date: " + fromdate_ + " to " + todate_,]+ [""] * 9 + ["Shift: " + shift_header],
            [""],
            ["Employee category / Department", "Staff", "", "JOE", "", "Tech", "", "Trainee", "", "NAPS", "",
             "Contract(CL)", "", "New Joining Trainees", "", "Temporary CL","", "Total Plan","Total Actual",
            "","","","Cummulative Actual","Absent Gap (Plan-Actual)","Informed Leave(HRMS request approved)",""," Un informed Leave(HRMS request not approved)","","Total Gap",
            "Requested manpower","Given manpower","Remarks"],
            [""],
            [""],
            ["", "Plan", "Actual", "Plan", "Actual", "Plan", "Actual", "Plan", "Actual", "Plan", "Actual",
            "Plan", "Actual", "Plan", "Actual", "Plan","Actual","","Present","","","",],
            ["",]+[""]*17+ ["Actual Present","Permission","Miss Punch","OD"]
        ]
        if not args.get('shift'):
            # shift = ["in", [1, 2]]
            shift = ["is","set"]
        else:
            shift = args.get('shift')
        departments = frappe.get_all('Department', filters={'disabled': 0}, order_by='name asc')
        total_planning_staff,total_plan_cl ,total_plan_dt, total_plan_iti,total_plan_naps,total_plan_trainee = 0,0,0,0,0,0
        total_actual_dt,total_actual_staff,total_actual_naps,total_actual_iti,total_actual_cl, total_actual_trainee =0, 0,0,0,0,0
        total_cumulative,total_coff,total_absent_gap,total_of_total_gap,total_od,total_permission,actual_leave,plan_leave,total_misspunch = 0,0,0,0,0,0,0,0,0
        total_plan_total,total_actual_total =0, 0
        total_plan_access_card, total_actual_access_card =0,0
        total_plan_new_joinee,total_actual_new_joinee = 0,0
        total_cl_access_card_actual =0
        # total_new_trainee_and_staff_plan_access_card,total_new_trainee_and_staff_actual_access_card = 0,0
        for dept in departments:
            remarks = ""
            if dept.name != "All Departments":
                conditions = {
                    'department': dept.name,
                    'shift': shift,
                    'attendance_date': ["between",[start_date, end_date]],
                    'docstatus':['!=',2]
                }
                planed_emp = frappe.db.get_all("Shift Assignment",{'department': dept.name,'start_date': ["between",[start_date, end_date]],'shift_type':shift,'docstatus': 1,'employee_category': ['in',['Staff','Manager','ITI','TT','Naps','CL','GT','New CL','New Staff','New Trainees']]},pluck="employee")
                present_emp = frappe.db.get_all("Attendance",{**conditions, 'category': ['in',['Staff','Manager','ITI','TT','Naps','CL','GT','New CL','New Staff','New Trainees']]},pluck="employee" )
                for i in planed_emp:
                    if i not in present_emp:
                        emp_name = frappe.db.get_value("Employee",i,"employee_name")
                        if remarks =='':
                            remarks+=f"{i} : {emp_name}"
                        else:
                            remarks+=f", {i} : {emp_name}"
                # Get employee categories and prepare row structure
                employee_categories = frappe.get_all("Employee Category", fields=["name"], order_by='name')
                row = [dept.name]
                total_plan= 0
        
                plan_staff, actual_staff, plan_cl, plan_dt, plan_gt, plan_iti, plan_naps, actual_cl, actual_dt, actual_new_joinee, actual_access_card = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                plan_tt, actual_tt, actual_gt, actual_iti, actual_naps, actual_trainee, plan_trainee, plan_new_joinee, plan_access_card = 0, 0, 0, 0, 0, 0, 0, 0, 0
                actual_total_permission, actual_total_misspunch, actual_total_coff, actual_total_od, actual_total_absent_gap, actual_total_cumulative = 0, 0, 0, 0, 0, 0
                actual_total_leave_application, total_leave_application_not_approved, total_gap = 0, 0, 0
                new_trainee_plan_access_card,new_staff_plan_access_card,new_staff_actual_access_card,new_trainee_actual_access_card =0,0,0,0
                # new_trainee_and_staff_plan_access_card,new_trainee_and_staff_actual_access_card = 0,0
                cl_access_card_actual,cl_access_card_plan =0,0
                # Loop through employee categories
                for emp_category in employee_categories:
                    emp_category_name = emp_category['name']
                    plan_field = 'employee_category'
                    actual_field = 'category'
                    # conditions = {
                    #     'department': dept.name,
                    #     'shift': shift,
                    #     'attendance_date': ["between",[start_date, end_date]],
                    #     'docstatus':['!=',2]
                    # }

                    if emp_category_name == "Staff":
                        plan_staff = frappe.db.count("Shift Assignment", {
                            'department': dept.name,
                            plan_field: emp_category_name,
                            'start_date': ["between",[start_date, end_date]],
                            'shift_type':shift,
                            'docstatus': 1
                        })
                        actual_staff = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    elif emp_category_name == "DT":
                        plan_dt = frappe.db.count("Shift Assignment", {
                            'department': dept.name,
                            plan_field: emp_category_name,
                            'start_date': ["between",[start_date, end_date]],
                            'shift_type':shift,
                            'docstatus': 1
                        })
                        actual_dt = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    elif emp_category_name == "ITI":
                        plan_iti = frappe.db.count("Shift Assignment", {
                            'department': dept.name,
                            plan_field: emp_category_name,
                            'start_date': ["between",[start_date, end_date]],
                            'shift_type':shift,
                            'docstatus': 1
                        })
                        actual_iti = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    elif emp_category_name == "TT":
                        plan_tt = frappe.db.count("Shift Assignment", {
                            'department': dept.name,
                            plan_field: emp_category_name,
                            'start_date': ["between",[start_date, end_date]],
                            'shift_type':shift,
                            'docstatus': 1
                        })
                        actual_tt = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    elif emp_category_name == "Naps":
                        plan_naps = frappe.db.count("Shift Assignment", {
                            'department': dept.name,
                            plan_field: emp_category_name,
                            'start_date': ["between",[start_date, end_date]],
                            'shift_type':shift,
                            'docstatus': 1
                        })
                        actual_naps = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    elif emp_category_name == "CL":
                        plan_cl = frappe.db.count("Shift Assignment", {
                            'department': dept.name,
                            plan_field: emp_category_name,
                            'start_date': ["between",[start_date, end_date]],
                            'shift_type':shift,
                            'docstatus': 1
                        })
                        actual_cl = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    elif emp_category_name == "GT":
                        plan_gt = frappe.db.count("Shift Assignment", {
                            'department': dept.name,
                            plan_field: emp_category_name,
                            'start_date': ["between",[start_date, end_date]],
                            'shift_type':shift,
                            'docstatus': 1
                        })
                        actual_gt = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})

                    elif emp_category_name == "New CL":
                        plan_access_card = frappe.db.count("Shift Assignment", {
                            'department': dept.name,
                            plan_field: emp_category_name,
                            'start_date': ["between",[start_date, end_date]],
                            'shift_type':shift,
                            'docstatus': 1
                        })
                        actual_access_card = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    elif emp_category_name == "New Staff":
                        new_staff_plan_access_card = frappe.db.count("Shift Assignment", {
                            'department': dept.name,
                            plan_field: emp_category_name,
                            'start_date': ["between",[start_date, end_date]],
                            'shift_type':shift,
                            'docstatus': 1
                        })
                        new_staff_actual_access_card = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    elif emp_category_name == "New Trainees":
                        new_trainee_plan_access_card = frappe.db.count("Shift Assignment", {
                            'department': dept.name,
                            plan_field: emp_category_name,
                            'start_date': ["between",[start_date, end_date]],
                            'shift_type':shift,
                            'docstatus': 1
                        })
                        new_trainee_actual_access_card = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    elif emp_category_name == "CL (Access Card)":
                        cl_access_card_plan = frappe.db.count("Shift Assignment", {
                            'department': dept.name,
                            plan_field: emp_category_name,
                            'start_date': ["between",[start_date, end_date]],
                            'shift_type':shift,
                            'docstatus': 1
                        })
                        cl_access_card_actual = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    
                plan_new_joinee = new_trainee_plan_access_card + new_staff_plan_access_card
                actual_new_joinee = new_staff_actual_access_card + new_trainee_actual_access_card
                
                actual_trainee = actual_gt + actual_tt
                plan_trainee = plan_gt + plan_tt
                plan_total = frappe.db.count("Shift Assignment", {
                    'department': dept.name,
                    'start_date': ["between",[start_date, end_date]],
                    'shift_type':shift,
                    'employee_category': ('not in', ['CL (Access Card)']),
                    'docstatus': 1
                })
                actual_total = frappe.db.count("Attendance", {
                    'department': dept.name,
                    'shift': shift,
                    'category': ('not in', ['CL (Access Card)']),
                    'attendance_date': ["between",[start_date, end_date]],
                    'docstatus':['!=',2]
                })
                
                actual_total_permission = frappe.db.count("Attendance", {
                    'department': dept.name,
                    'shift': shift,
                    'permission': ["!=", ""],
                    'category': ('not in', ['CL (Access Card)']),
                    'attendance_date': ["between", [start_date, end_date]],
                    'docstatus':['!=',2]
                })
                actual_total_misspunch = frappe.db.count("Attendance", {
                    'department': dept.name,
                    'shift': shift,
                    'miss_punch': ["!=", ""],
                    'category': ('not in', ['CL (Access Card)']),
                    'attendance_date': ["between", [start_date, end_date]],
                    'docstatus':['!=',2]
                })
                
                actual_total_od = frappe.db.count("Attendance", {
                    'department': dept.name,
                    'shift': shift,
                    'on_duty_application': ["!=", ""],
                    'category': ('not in', ['CL (Access Card)']),
                    'attendance_date': ["between", [start_date, end_date]],
                    'docstatus':['!=',2]
                })
                approved_leaves = frappe.db.get_all(
                    "Attendance",
                    {
                        'department': dept.name,
                        'leave_application': ["!=", ""],  
                        'attendance_date': ["between", [start_date, end_date]] ,
                        'category': ('not in', ['CL (Access Card)']),
                        'docstatus':['!=',2]     
                    },
                    ['employee','attendance_date']  
                )
                for leave in approved_leaves:
                    shift_count_leaves = frappe.db.count(
                        'Shift Assignment',
                        {
                            'employee': leave.employee,       
                            'start_date': leave.attendance_date,         
                            'employee_category': ('not in', ['CL (Access Card)']),
                            'shift_type': shift,              
                            'docstatus': ('!=', 2)           
                        }
                    )
                    
                    actual_total_leave_application += shift_count_leaves

                dates = pd.date_range(start=start_date, end=end_date)
                for date in dates:
                    not_approved_leaves = frappe.db.sql("""
                        select employee
                        from `tabLeave Application`
                        where docstatus = 0 and department = %(department)s
                            and (from_date between %(from_date)s and %(to_date)s
                                or to_date between %(from_date)s and %(to_date)s
                                or (from_date < %(from_date)s and to_date > %(to_date)s))
                        """, {
                            "from_date": date,
                            "to_date": date,
                            "department":dept.name
                        },
                    as_dict = True)
                    for leave in not_approved_leaves:
                        shift_count_leaves_ = frappe.db.count(
                            'Shift Assignment',
                            {
                                'employee': leave['employee'],       
                                'start_date': date,       
                                'employee_category': ('not in', ['CL (Access Card)']),
                                'shift_type': shift,              
                                'docstatus': ('!=', 2)           
                            }
                        )
                        total_leave_application_not_approved += shift_count_leaves_
                actual_total_cumulative = actual_total + actual_total_misspunch + actual_total_permission + actual_total_od
                actual_total_absent_gap = plan_total - actual_total_cumulative
                total_gap = total_leave_application_not_approved + actual_total_leave_application
                row.extend([plan_staff, actual_staff, plan_dt, actual_dt, plan_iti, actual_iti, plan_trainee, actual_trainee,
                            plan_naps, actual_naps, plan_cl, actual_cl, plan_new_joinee, actual_new_joinee, plan_access_card,
                            actual_access_card])
                total_planning_staff += plan_staff 
                total_actual_staff += actual_staff
                total_plan_dt += plan_dt
                total_actual_dt += actual_dt
                total_plan_iti += plan_iti
                total_plan_trainee += plan_trainee
                total_plan_naps +=plan_naps
                total_plan_cl += plan_cl
                total_actual_iti += actual_iti
                total_actual_trainee += actual_trainee
                total_actual_naps += actual_naps
                total_actual_cl += actual_cl
                plan_leave += actual_total_leave_application
                actual_leave += total_leave_application_not_approved
                total_of_total_gap +=total_gap
                total_permission += actual_total_permission
                total_misspunch += actual_total_misspunch
                total_od += actual_total_od
                total_coff += actual_total_coff
                total_plan_total +=plan_total
                total_actual_total += actual_total
                total_cumulative += actual_total_cumulative
                total_absent_gap += actual_total_absent_gap
                total_plan_access_card +=plan_access_card
                total_actual_access_card +=actual_access_card
                total_actual_new_joinee +=actual_new_joinee
                total_plan_new_joinee+=plan_new_joinee
                total_cl_access_card_actual += cl_access_card_actual
                row.append(plan_total)
                row.append(actual_total)
                row.append(actual_total_permission)
                row.append(actual_total_misspunch)
                # row.append(actual_total_coff)
                row.append(actual_total_od)
                row.append(actual_total_cumulative)
                row.append(actual_total_absent_gap)
                row.append(actual_total_leave_application)
                row.append("")
                row.append(total_leave_application_not_approved)
                row.append("")
                row.append(total_gap)
                row.append("")
                row.append(cl_access_card_actual)
                row.append(remarks)
                data.append(row)
        extra_row = [
            "Totals", total_planning_staff, total_actual_staff, total_plan_dt, total_actual_dt, total_plan_iti, 
            total_actual_iti, total_plan_trainee, total_actual_trainee, total_plan_naps, total_actual_naps, 
            total_plan_cl, total_actual_cl, total_plan_new_joinee, total_actual_new_joinee, total_plan_access_card, total_actual_access_card, 
            total_plan_total, total_actual_total, total_permission, total_misspunch, total_od, total_cumulative, total_absent_gap, plan_leave, "", 
            actual_leave, "", total_of_total_gap,"",total_cl_access_card_actual
        ]
        # extra_row = ["Totals", total_planning_staff, total_actual_staff,total_plan_dt, total_actual_dt, total_plan_iti, total_actual_iti, total_plan_trainee, total_actual_trainee, total_plan_naps, total_actual_naps, total_plan_cl, total_actual_cl,
        # 0,0,0,0,total_permission,total_misspunch,total_od,total_coff,total_plan_total,total_actual_total,total_cumulative,total_absent_gap,plan_leave,"",actual_leave,"",total_of_total_gap]
        data.append(extra_row)

        return data
    
    