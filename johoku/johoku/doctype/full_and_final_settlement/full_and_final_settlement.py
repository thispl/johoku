# # Copyright (c) 2026, TEAMPRO and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document
# from frappe.utils import ceil, flt
# from frappe.utils import getdate

# class FullandFinalSettlement(Document):
#     pass

# @frappe.whitelist()
# def get_salary_details(employee, relieving_date, fixed_basic=0, working_days=0,el_leave_days=0):
#     if not employee or not relieving_date:
#         return {}

#     # Get Salary Slip based on relieving date
#     salary_slip = frappe.get_all(
#         "Salary Slip",
#         filters={
#             "employee": employee,
#             "start_date": ["<=", relieving_date],
#             "end_date": [">=", relieving_date],
#             "docstatus": 1
#         },
#         fields=["name", "payment_days", "absent_days", "leave_without_pay", "total_working_days"]
#     )

#     if not salary_slip:
#         return {}

#     slip = salary_slip[0]
#     doc = frappe.get_doc("Salary Slip", slip.name)

# # Convert safely
#     fixed_basic = flt(fixed_basic)
#     working_days = flt(working_days)
#     el_leave_days = flt(el_leave_days)

#     penalty_amount = 0
#     if working_days > 0:
#         payment_days = flt(slip.payment_days)
#         penalty_amount = ceil((fixed_basic / working_days) * payment_days)

#     el_amount = 0
#     if working_days > 0:
#         el_amount = ceil((fixed_basic / working_days) * el_leave_days)

    
#     return {
#         "payment_days": slip.payment_days or 0,
#         "total_working_days": slip.total_working_days or 0,
#         "lop_days": (slip.absent_days or 0) + (slip.leave_without_pay or 0),
#         "earnings": [
#             {
#                 "salary_component": e.salary_component,
#                 "earned_amount": e.amount
#             } for e in doc.earnings
#         ] + ([{
#             "salary_component": "EL Encashment",
#             "earned_amount": el_amount
#         }] if el_amount > 0 else []),
#         "deductions": [
#             {
#                 "salary_component": d.salary_component,
#                 "deductions_amount": d.amount
#             } for d in doc.deductions
#         ] + ([{
#             "salary_component": "Penalty",
#             "deductions_amount": penalty_amount
#         }] if penalty_amount > 0 else [])
        
        
#     }
    
    


# @frappe.whitelist()
# def get_el_leave_balance(employee, relieving_date):
#     if not employee or not relieving_date:
#         return 0

#     rel_date = getdate(relieving_date)
#     year = rel_date.year

#     def get_values(year):
#         allocation = frappe.db.sql("""
#             SELECT SUM(total_leaves_allocated)
#             FROM `tabLeave Allocation`
#             WHERE employee = %s
#             AND leave_type = 'Earned Leave'
#             AND docstatus = 1
#             AND YEAR(from_date) = %s
#         """, (employee, year))[0][0] or 0

#         leaves_taken = frappe.db.sql("""
#             SELECT SUM(total_leave_days)
#             FROM `tabLeave Application`
#             WHERE employee = %s
#             AND leave_type = 'Earned Leave'
#             AND status = 'Approved'
#             AND docstatus = 1
#             AND YEAR(from_date) = %s
#         """, (employee, year))[0][0] or 0

#         return allocation, leaves_taken

#     allocation, leaves_taken = get_values(year)

#     if allocation == 0:
#         prev_year = year - 1
#         allocation, leaves_taken = get_values(prev_year)

#     el_balance = allocation - leaves_taken

#     return el_balance

# Copyright (c) 2026, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import ceil, flt, getdate
from datetime import datetime, timedelta
import calendar

class FullandFinalSettlement(Document):
    def validate(self):
        existing = frappe.db.exists(
            "Full and Final Settlement",
            {
                "employee": self.employee,
                "docstatus": ["!=", 2],
                "name": ["!=", self.name]
            }
        )

        if existing:
            frappe.throw(
                f"Full & Final Settlement already exists for Employee {self.employee}: {existing}"
            )


@frappe.whitelist()
def get_salary_details(employee, relieving_date, fixed_basic=0, working_days=0, el_leave_days=0):
    if not employee or not relieving_date:
        return {}

    # Get Salary Slip based on relieving date
    # salary_slip = frappe.get_all(
    #     "Salary Slip",
    #     filters={
    #         "employee": employee,
    #         "start_date": ["<=", relieving_date],
    #         "end_date": ["<=", relieving_date],
    #         "docstatus": 1 
    #     },
    #     fields=["name", "payment_days", "absent_days", "leave_without_pay", "total_working_days"]
    # )

    # if not salary_slip:
    #     frappe.throw(
    #      f"Salary Slip not found for Employee {employee} on relieving date {relieving_date}. Please create and submit the Salary Slip."
    # )

    # slip = salary_slip[0]
    salary_slip = frappe.get_all(
        "Salary Slip",
        filters={
            "employee": employee,
            "end_date": ["<=", relieving_date],
            "docstatus": 1
        },
        fields=["name", "payment_days", "absent_days", "leave_without_pay", "total_working_days", "end_date"],
        order_by="end_date desc",
        limit=1
    )

    if not salary_slip:
        frappe.throw(
            f"Salary Slip not found for Employee {employee} on relieving date {relieving_date}. Please create and submit the Salary Slip."
        )

    slip = salary_slip[0]
    doc = frappe.get_doc("Salary Slip", slip.name)

    mis = frappe.get_value(
        "Employee",
        employee,
        ["basic", "house_rent_allowance", "special_allowance","conveyance_allowance"],
        as_dict=True
    )
    frappe.errprint(f"MIS: {mis}")
    component_map = {
        "Basic": "basic",
        "House Rent Allowance": "house_rent_allowance",
        "Special Allowance": "special_allowance",
        "Conveyance Allowance": "conveyance_allowance"   
    }

    fixed_basic = flt(fixed_basic)
    working_days = flt(working_days)
    el_leave_days = flt(el_leave_days)
    
    
    
    
    penalty_amount = 0
    if working_days > 0:
        payment_days = flt(slip.payment_days)
        penalty_amount = ceil((fixed_basic / working_days) * payment_days)

    el_amount = 0
    if working_days > 0:
        el_amount = ceil((fixed_basic / working_days) * el_leave_days)

    # earnings_list = [
    #     {
    #         "salary_component": e.salary_component,
    #         "earned_amount": flt(e.amount)
    #     }
    #     for e in doc.earnings
    # ]
    earnings_list = []

    for e in doc.earnings:
        comp_name = e.salary_component
        frappe.errprint(f"Component: {comp_name}")
        fixed_amt = 0
        if mis and comp_name in component_map:
            fieldname = component_map[comp_name]
            fixed_amt = flt(mis.get(fieldname))

        earnings_list.append({
            "salary_component": comp_name,
            "earned_amount": flt(e.amount),
            "fixed_amount": fixed_amt 
        })

    # Add EL Encashment
    # if el_amount > 0:
    #    earnings_list.append({
    #         "salary_component": "EL Encashment",
    #         "earned_amount": el_amount
    #     }) 
    if el_amount > 0:
        earnings_list.append({
            "salary_component": "EL Encashment",
            "earned_amount": el_amount,
            "fixed_amount": 0
        })
    
    


    deductions_list = [
        {
            "salary_component": d.salary_component,
            "deductions_amount": (
                flt(d.amount) * 2
                if d.salary_component == "Professional Tax" and doc.total_working_days == 45
                else flt(d.amount)
            )
        }
        for d in doc.deductions
    ]
    

    total_payable = sum(flt(e["earned_amount"]) for e in earnings_list)
    total_receivable = sum(flt(d["deductions_amount"]) for d in deductions_list)
    net_amount = total_payable - total_receivable

    return {
        "payment_days": slip.payment_days or 0,
        "total_working_days": slip.total_working_days or 0,
        "lop_days": (slip.absent_days or 0) + (slip.leave_without_pay or 0),
        "earnings": earnings_list,
        "deductions": deductions_list,
        "total_payable_amount": total_payable,
        "total_receivable_amount": total_receivable,
    }


@frappe.whitelist()
def get_el_leave_balance(employee, relieving_date):
    if not employee or not relieving_date:
        return 0

    rel_date = getdate(relieving_date)
    year = rel_date.year

    def get_values(year):
        allocation = frappe.db.sql("""
            SELECT SUM(total_leaves_allocated)
            FROM `tabLeave Allocation`
            WHERE employee = %s
            AND leave_type = 'Earned Leave'
            AND docstatus = 1
            AND YEAR(from_date) = %s
        """, (employee, year))[0][0] or 0

        leaves_taken = frappe.db.sql("""
            SELECT SUM(total_leave_days)
            FROM `tabLeave Application`
            WHERE employee = %s
            AND leave_type = 'Earned Leave'
            AND status = 'Approved'
            AND docstatus = 1
            AND YEAR(from_date) = %s
        """, (employee, year))[0][0] or 0

        return allocation, leaves_taken

    allocation, leaves_taken = get_values(year)

    if allocation == 0:
        prev_year = year - 1
        allocation, leaves_taken = get_values(prev_year)

    el_balance = allocation - leaves_taken

    return el_balance

@frappe.whitelist()
def this_month_salary(employee, relieving_date, days_worked):

    from frappe.utils import flt

    days_worked = flt(days_worked)

    salary_slip = frappe.get_all(
        "Salary Slip",
        filters={
            "employee": employee,
            "end_date": ["<=", relieving_date],
            "docstatus": 1
        },
        fields=["name", "end_date"],
        order_by="end_date desc",
        limit=1
    )

    if not salary_slip:
        frappe.throw("No Salary Slip found")

    slip_end = salary_slip[0].end_date

    next_start = frappe.utils.add_days(slip_end, 1)
    next_end = frappe.utils.add_months(slip_end, 1)
    next_end = next_end.replace(day=20)
    frappe.errprint("next start")
    frappe.errprint(next_start)
    frappe.errprint("next end")
    frappe.errprint(next_end)
    total_day = (next_end - next_start).days + 1
    
    frappe.errprint("total_day")
    frappe.errprint(total_day)
    mis = frappe.get_value(
        "Employee",
        employee,
        ["basic", "house_rent_allowance", "special_allowance", "conveyance_allowance"],
        as_dict=True
    ) or {}

    component_map = {
        "Basic": "basic",
        "House Rent Allowance": "house_rent_allowance",
        "Special Allowance": "special_allowance",
        "Conveyance Allowance": "conveyance_allowance"
    }

    earnings_list = []

    for comp, field in component_map.items():

        fixed_amt = flt(mis.get(field))
        frappe.errprint("fixed_amt")
        frappe.errprint(fixed_amt)
        frappe.errprint("days_worked")
        frappe.errprint(days_worked)
        prorated = (fixed_amt / flt(total_day)) * flt(days_worked)
        frappe.errprint("prorated")
        frappe.errprint(prorated)
        final_amount = fixed_amt + prorated
        frappe.errprint("final_amount")
        frappe.errprint(final_amount)
        earnings_list.append({
            "salary_component": comp,
            "fixed_amount": fixed_amt,
            "prorated_amount": flt(prorated),
            "earned_amount": flt(final_amount)
        })
        frappe.errprint(earnings_list)

    return {
        "cycle_days": total_day,
        "days_worked": days_worked,
        "earnings": earnings_list
    }
