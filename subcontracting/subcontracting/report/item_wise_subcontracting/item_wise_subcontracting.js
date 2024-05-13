// Copyright (c) 2024, Muhammed ibnu arif and contributors
// For license information, please see license.txt
/* eslint-disable */



frappe.query_reports["Item-wise Subcontracting"] = {
	filters: [

		{
			fieldname: "from_date",
			reqd: 1,
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname: "to_date",
			reqd: 1,
			default: frappe.datetime.get_today(),
			label: __("To Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group",
		},
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
		},
		{
			fieldname: "subcontarctor",
			label: __("Sub-Contractor"),
			fieldtype: "Link",
			options: "Sub-Contractor",
		},
	],

};