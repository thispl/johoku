frappe.query_reports["Department Wise Employee Trend Count"] = {
    "filters": [
        {
            "fieldname": "start_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd": 1,
            "default": frappe.datetime.month_start()
        },
        {
            "fieldname": "end_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd": 1,
            "default": frappe.datetime.month_end()
        },
        {
            "fieldname": "shift",
            "label": __("Shift"),
            "fieldtype": "Link",
            "options": "Shift Type",
            "default": "1"
        },
        {
            "fieldname": "department",
            "label": __("Department"),
            "fieldtype": "Link",
            "options": "Department"
        }
    ],
    onload: function(report) {
        frappe.call({
            method: "johoku.johoku.report.department_wise_employee_trend_count.department_wise_employee_trend_count.get_chart_data",
            args: {
                filters: report.get_filter_values()
            },
            callback: function(response) {
                if (response.message) {
                    const chart_data = response.message.chart;
                    if (chart_data.labels.length && chart_data.datasets.length) {
                        report.chart = {
                            data: chart_data,
                            type: "line", // Chart type: 'line', 'bar', 'pie', etc.
                            height: 100
                        };
                        report.append(chart);
                    } else {
                        frappe.msgprint({
                            title: __("No Data"),
                            message: __("No chart data available for the selected filters."),
                            indicator: "orange"
                        });
                    }
                }
            }
        });
    }
};
