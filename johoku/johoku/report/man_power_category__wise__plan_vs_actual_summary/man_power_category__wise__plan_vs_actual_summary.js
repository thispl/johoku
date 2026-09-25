// Copyright (c) 2024, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Man Power Category  Wise  Plan Vs Actual Summary"] = {
	"filters": [
		{
			"fieldname": "date",
			"label":__("Date"),
			"fieldtype": "Date",
			// "reqd": 1,
		},
		{
			"fieldname": "shift",
			"label":__("Shift Type"),
			"fieldtype": "Link",
			"options": "Shift Type",
		}
	]
};
