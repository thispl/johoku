# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("Department"),
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department",
            "width": 150
        },
        {
			"label": _("Staff"),
            "fieldname": "staff",
            "fieldtype": "Data",
            "width": 150
		},
         {
			"label": _("JOE"),
            "fieldname": "joe",
            "fieldtype": "Data",
            "width": 150
		},
        {
			"label": _("Tech"),
            "fieldname": "tech",
            "fieldtype": "Data",
            "width": 150
		},
        {
			"label": _("Trainee"),
            "fieldname": "trainee",
            "fieldtype": "Data",
            "width": 150
		},
        {
			"label": _("NAPS"),
            "fieldname": "naps",
            "fieldtype": "Data",
            "width": 150
		},
        {
			"label": _("Contract(CL)"),
            "fieldname": "contract_cl",
            "fieldtype": "Data",
            "width": 150
		},
        {
			"label": _("New Joining(Dept wise access card)"),
            "fieldname": "new_joining",
            "fieldtype": "Data",
            "width": 150
		},
        {
			"label": _("Additional CL Plan (Contractors wise access card)"),
            "fieldname": "additional_cl",
            "fieldtype": "Data",
            "width": 150
		},
        {
			"label": _("Total Plan"),
            "fieldname": "total_plan",
            "fieldtype": "Data",
            "width": 150
		},
    ]
    
    

    return columns

def get_data(filters):
    data = []
    row = []
    departments = frappe.db.get_all("Department", {"disabled": 0}, ["name"], order_by='name')
    employee_categories = frappe.get_all("Employee Category", ["name"], order_by='name')
    for dept in departments:
        
        row = [dept.name, '1', '2', '3', '4', '5', '6', '7', '8', 9]

        data.append(row)

    return data
