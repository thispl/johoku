// Copyright (c) 2024, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Attendance Register - Employee"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "default":frappe.datetime.year_start()
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "default":frappe.datetime.year_end()
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"reqd": 1,
		},
		// {
		// 	"fieldname": "department",
		// 	"label": __("Department"),
		// 	"fieldtype": "Link",
		// 	"options": "Department",
		// },
		// {
		// 	"fieldname": "work_station",
		// 	"label": __("Work Station"),
		// 	"fieldtype": "Link",
		// 	"options": "Work Station"
		// },
		// {
		// 	"fieldname": "employee_category",
		// 	"label": __("Employee Category"),
		// 	"fieldtype": "Link",
		// 	"options":"Employee Category"
		// },
	],
	onload: function (report) {
		var to_date = frappe.query_report.get_filter('to_date');
		to_date.refresh();
		var c = frappe.datetime.add_months(frappe.datetime.month_start(), 1)
		to_date.set_input(frappe.datetime.add_days(c, 19))
		var from_date = frappe.query_report.get_filter('from_date');
		from_date.refresh();
		var d = frappe.datetime.add_months(frappe.datetime.month_start(), 0)
		from_date.set_input(frappe.datetime.add_days(d, 20))
		frappe.db.get_value("Employee", {'user_id': frappe.session.user}, ['employee'], (r) => {
			if (r && r.employee) {
				// Set the 'employee' field to the logged-in user's employee
				frappe.query_report.set_filter_value('employee', r.employee);
			}
		});
	}	
};
