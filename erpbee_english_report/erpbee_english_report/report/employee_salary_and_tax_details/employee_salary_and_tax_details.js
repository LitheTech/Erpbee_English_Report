// Copyright (c) 2025, LTL and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Salary and Tax Details"] = {
	"filters": [
		// {
		// 	"fieldname":"from_date",
		// 	"label": __("From"),
		// 	"fieldtype": "Date",
		// 	"default": frappe.datetime.add_months(frappe.datetime.get_today(),-1),
		// 	"reqd": 1,
		// 	"width": "100px"
		// },
		// {
		// 	"fieldname":"to_date",
		// 	"label": __("To"),
		// 	"fieldtype": "Date",
		// 	"default": frappe.datetime.get_today(),
		// 	"reqd": 1,
		// 	"width": "100px"
		// },
		{
			"fieldname": "employee",
			"fieldtype": "Link",
			"label": "Employee",
			// "mandatory": 1,
			"options": "Employee",
			"wildcard_filter": 0
		},
		{
			"fieldname": "income_year",
			"fieldtype": "Link",
			"label": "Income Year",
			// "mandatory": 1,
			"options": "Fiscal Year",
			"wildcard_filter": 0
		},

	]
};
