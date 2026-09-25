// Copyright (c) 2024, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Register Reports', {
	// refresh: function(frm) {

	// }
	download(frm) {
		if (frm.doc.report === 'Salary Register for Staff') {
			if (frm.doc.from_date && frm.doc.to_date) {  // Ensure both date and shift are present
				var path = 'johoku.johoku.doctype.salary_register_reports.salary_details_staff_staff.download';
				var args = "from_date=" + encodeURIComponent(frm.doc.from_date) +
					"&to_date=" + encodeURIComponent(frm.doc.to_date);  // Include shift in args
			}
		}
		if (frm.doc.report === 'Salary Register for GT') {
			if (frm.doc.from_date && frm.doc.to_date) {  // Ensure both date and shift are present
				var path = 'johoku.johoku.doctype.salary_register_reports.gt_report.download';
				var args = "from_date=" + encodeURIComponent(frm.doc.from_date) +
					"&to_date=" + encodeURIComponent(frm.doc.to_date);  // Include shift in args
			}
		}
		if (frm.doc.report === 'Salary register for TT') {
				if (frm.doc.from_date && frm.doc.to_date) {  // Ensure both date and shift are present
					var path = 'johoku.johoku.doctype.salary_register_reports.tt_salary_registers.download';
					var args = "from_date=" + encodeURIComponent(frm.doc.from_date) +
						"&to_date=" + encodeURIComponent(frm.doc.to_date);  
				}
		}
		if (frm.doc.report === 'Salary Register for ITI') {
			if (frm.doc.from_date && frm.doc.to_date) {// Ensure both date and shift are present
				var path = 'johoku.johoku.doctype.salary_register_reports.iti_report.download';
				var args = "from_date=" + encodeURIComponent(frm.doc.from_date) +
					"&to_date=" + encodeURIComponent(frm.doc.to_date);  
			}
		}
		if (frm.doc.report === 'Salary Register for DT') {
			if (frm.doc.from_date && frm.doc.to_date) {// Ensure both date and shift are present
				var path = 'johoku.johoku.doctype.salary_register_reports.salary_reports_dt.download';
				var args = "from_date=" + encodeURIComponent(frm.doc.from_date) +
					"&to_date=" + encodeURIComponent(frm.doc.to_date);  
			}
		}
		if (frm.doc.report === 'Salary Summary') {
			if (frm.doc.from_date && frm.doc.to_date) {// Ensure both date and shift are present
				var path = 'johoku.johoku.doctype.report_dashboard.salary_summary_reports.download';
				var args = "from_date=" + encodeURIComponent(frm.doc.from_date) +
					"&to_date=" + encodeURIComponent(frm.doc.to_date);  
			}
		}
		if (path && args) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				from_date:frm.doc.from_date,
				to_date:frm.doc.to_date
			});
		}
	
	}
});
