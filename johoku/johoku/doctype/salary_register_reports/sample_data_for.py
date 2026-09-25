import frappe
from frappe.model.document import Document
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from six import BytesIO
from datetime import datetime
from frappe.utils import getdate, nowdate, format_date

class SalaryRegisterReport(Document):
    pass

@frappe.whitelist()
def download():
    filename = 'Salary_Register_Reports'
    build_xlsx_response(filename)

def apply_common_styles(cell,header_font_data, align_center, border):
    """Apply common styles like alignment and borders to a cell."""
    cell.alignment = align_center

def apply_header_styles(ws, header_font, align_center, border):
    """Apply header styles like font, alignment, fill color, and borders."""
    header_fill = PatternFill(fgColor="002060", fill_type="solid")
    
    for cell in ws[1]:  # Apply to the header row
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_center
        cell.border = border

def set_column_widths(ws):
    """Set the column widths for the Excel sheet."""
    column_widths = [5, 20, 30, 20, 20, 10, 10, 15, 15, 15, 5]
    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

def make_xlsx(sheet_name='Sheet1'):
    args = frappe.local.form_dict
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    # Create headers
    headerrow = ["S#", "E-Code", "Employee Name", "DOJ", "Designation", "Fixed", "PD", "Gross", "Deduction", "Net", "B"]
    ws.append(headerrow)

    # Define common styles
    align_center = Alignment(horizontal='center', vertical='center', wrap_text=False)
    align_left = Alignment(horizontal='left', vertical='top', wrap_text=True)
    header_font = Font(color="FFFFFF", bold=True, size=14)
    header_font_data = Font(color="002060", bold=True, size=14)
    border = Border(
        left=Side(border_style='thin'),
        right=Side(border_style='thin'),
        top=Side(border_style='thin'),
        bottom=Side(border_style='thin')
    )

    # Apply header styles
    apply_header_styles(ws, header_font, align_center, border)

    # Set column widths
    set_column_widths(ws)

    from_date = args.get('from_date')
    to_date = args.get('to_date')

    if not from_date or not to_date:
        frappe.throw("From Date and To Date are required.")

    departments = frappe.get_all(
        "Department", 
        {"disabled": 0, 'is_group': 1, "name": ["!=", "All Departments"]}, 
        ["name"], 
        order_by="name asc"
    )

    index = 0
    for dept in departments:
        child_departments = frappe.get_all(
            "Department", 
            {"disabled": 0, "parent_department": dept.name}, 
            ["name"], 
            order_by="name asc"
        )
        
        department_names = [child_dept['name'] for child_dept in child_departments]

        total_fixed_salary = 0
        total_gross_salary = 0
        total_deduction = 0
        total_netpay = 0

        for dept_name in department_names:
            salary_slip_data = frappe.db.sql("""
                SELECT employee, salary_structure 
                FROM `tabSalary Slip`
                WHERE start_date = %s AND end_date = %s 
                AND docstatus != 2 AND department = %s 
                GROUP BY employee 
                ORDER BY employee
            """, (from_date, to_date, dept_name), as_dict=True)

            fixed_salary = 0
            for slip in salary_slip_data:
                fixed = frappe.db.get_value(
                    'Salary Structure Assignment',
                    {'employee': slip['employee'], 'salary_structure': slip['salary_structure'], 'docstatus': 1},
                    'base', order_by='creation desc'
                ) or 0.0
                fixed_salary += fixed

            total_fixed_salary += fixed_salary

        # Append the department summary row
        header_data = [
            dept.name,
            "",
            "",
            "",
            "",
            round(total_fixed_salary),
            "",
            round(total_gross_salary),
            round(total_deduction),
            round(total_netpay)
        ]
        ws.append(header_data)
        for cell in ws[ws.max_row]:
            apply_common_styles(cell,header_font_data, align_left, border)
            ws.merge_cells("A1:C1")
        # Process each child department
        for child_dept in child_departments:
            salary_slip_list_data = frappe.db.sql("""
                SELECT department, employee,
                    SUM(gross_pay) AS dept_gross_pay, 
                    SUM(total_deduction) AS dept_total_deduction, 
                    SUM(net_pay) AS dept_net_pay, 
                    salary_structure 
                FROM `tabSalary Slip`
                WHERE start_date = %s AND end_date = %s 
                AND docstatus != 2 AND department = %s 
                GROUP BY department 
                ORDER BY department DESC
            """, (from_date, to_date, child_dept.name), as_dict=True)

            for s in salary_slip_list_data:
                total_gross_salary += s['dept_gross_pay']
                total_deduction += s['dept_total_deduction']
                total_netpay += s['dept_net_pay']

                child_row = [
                    child_dept.name,
                    "",
                    "",
                    "",
                    "",
                    round(total_fixed_salary),
                    "",
                    round(s['dept_gross_pay']),
                    round(s['dept_total_deduction']),
                    round(s['dept_net_pay'])
                ]
                ws.append(child_row)

                # Apply styles to the child department row
                for cell in ws[ws.max_row]:
                    apply_common_styles(cell,header_font_data, align_left, border)
                    ws.merge_cells("A1:C1")

            # Process salary slips for each employee in the child department
            salary_slips = frappe.db.sql("""
                SELECT employee, employee_name, department, designation, payment_days, gross_pay, total_deduction, net_pay, salary_structure 
                FROM `tabSalary Slip`
                WHERE start_date = %s AND end_date = %s 
                AND docstatus != 2 AND department = %s 
                ORDER BY employee
            """, (from_date, to_date, child_dept.name), as_dict=True)

            for salary_slip in salary_slips:
                index += 1
                date_of_joining = frappe.db.get_value(
                    'Employee',
                    {'name': salary_slip['employee']},
                    'date_of_joining'
                )
                formatted_doj = datetime.strptime(str(date_of_joining), '%Y-%m-%d')
                doj = formatted_doj.strftime('%d-%m-%Y')
                fixed = frappe.db.get_value(
                    'Salary Structure Assignment',
                    {'employee': salary_slip['employee'], 'salary_structure': salary_slip['salary_structure']},
                    'base'
                ) or 0.0

                row = [
                    index,
                    salary_slip['employee'],
                    salary_slip['employee_name'],
                    doj,
                    salary_slip['designation'],
                    fixed,
                    salary_slip['payment_days'],
                    salary_slip['gross_pay'],
                    salary_slip['total_deduction'],
                    salary_slip['net_pay']
                ]
                ws.append(row)

                # Apply styles to the data row
                for cell in ws[ws.max_row]:
                    apply_common_styles(cell, header_font_data,align_center, border)
                

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file

def build_xlsx_response(filename):
    xlsx_file = make_xlsx(sheet_name=filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'
