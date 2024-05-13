# Copyright (c) 2024, Muhammed ibnu arif and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
from frappe.utils.nestedset import get_descendants_of


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date cannot be greater than To Date"))


	return None


def get_columns(filters):
	return [
		{
			"label": _("Item Code"),
			"fieldtype": "Link",
			"fieldname": "item_code",
			"options": "Item",
			"width": 120,
		},
		{"label": _("Item Name"), "fieldtype": "Data", "fieldname": "item_name", "width": 140},
		{
			"label": _("Item Group"),
			"fieldtype": "Data",
			"fieldname": "item_group",
			"options": "Item Group",
			"width": 120,
		},
		{"label": _("Quantity"), "fieldtype": "Float", "fieldname": "qty", "width": 150},
		{
			"label": _("Sub-Contracting"),
			"fieldtype": "Link",
			"fieldname": "sub_contracting",
			"options": "Sub-Contracting",
			"width": 100,
		},
		{
			"label": _("Date"),
			"fieldtype": "Date",
			"fieldname": "date",
			"width": 90,
		},
		{
			"label": _("Due Date"),
			"fieldtype": "Date",
			"fieldname": "due_date",
			"width": 90,
		},
		{
			"label": _("Sub-Contractor"),
			"fieldtype": "Link",
			"fieldname": "subcontarctor",
			"options": "Sub-Contractor",
			"width": 100,
		},
		# {
		# 	"label": _("Customer Group"),
		# 	"fieldtype": "Link",
		# 	"fieldname": "customer_group",
		# 	"options": "Customer Group",
		# 	"width": 120,
		# },
	]


def get_data(filters):
	data = []

	# customer_details = get_customer_details()
	# item_details = get_item_details()
	sales_order_records = get_sales_order_details(filters)

	for record in sales_order_records:
		# customer_record = customer_details.get(record.customer)
		row = {
			"item_code": record.get("item_code"),
			"item_name": record.get("item_name"),
			"item_group": record.get("item_group"),
			"quantity": record.get("qty"),
			"sub_contracting": record.get("name"),
			"date": record.get("date"),
			"due_date": record.get("due_date"),
			"subcontarctor": record.get("subcontarctor"),
		}
		data.append(row)

	return data


# def get_customer_details():
# 	details = frappe.get_all("Customer", fields=["name", "customer_name", "customer_group"])
# 	customer_details = {}
# 	for d in details:
# 		customer_details.setdefault(
# 			d.name, frappe._dict({"customer_name": d.customer_name, "customer_group": d.customer_group})
# 		)
# 	return customer_details


# def get_item_details():
# 	details = frappe.db.get_all("Item", fields=["name", "item_name"])
# 	item_details = {}
# 	for d in details:
# 		item_details.setdefault(d.name, frappe._dict({"item_name": d.item_name}))
# 	return item_details


def get_sales_order_details(filters):
    db_so = frappe.qb.DocType("Sub-Contracting")
    db_so_item = frappe.qb.DocType("Subcontracting-item")

    query = (
        frappe.qb.from_(db_so)
        .inner_join(db_so_item)
        .on(db_so_item.parent == db_so.name)
        .select(
            db_so.name,
            db_so.subcontarctor,
            db_so.date,
            db_so.due_date,
            db_so_item.item_code,
            db_so_item.item_name,
            db_so_item.item_group,
            db_so_item.qty,
        )
    )

    if filters.get("item_group"):
        query = query.where(db_so_item.item_group == filters.item_group)

    if filters.get("from_date"):
        query = query.where(db_so.date >= filters.from_date)

    if filters.get("to_date"):
        query = query.where(db_so.date <= filters.to_date)

    if filters.get("item_code"):
        query = query.where(db_so_item.item_code == filters.item_code)

    if filters.get("subcontarctor"):
        query = query.where(db_so.subcontarctor == filters.subcontarctor)

    return query.run(as_dict=1)



# def get_chart_data(data):
# 	item_wise_sales_map = {}
# 	labels, datapoints = [], []

# 	for row in data:
# 		item_key = row.get("item_code")

# 		if item_key not in item_wise_sales_map:
# 			item_wise_sales_map[item_key] = 0

# 		item_wise_sales_map[item_key] = flt(item_wise_sales_map[item_key]) + flt(row.get("amount"))

# 	item_wise_sales_map = {
# 		item: value for item, value in (sorted(item_wise_sales_map.items(), key=lambda i: i[1], reverse=True))
# 	}

# 	for key in item_wise_sales_map:
# 		labels.append(key)
# 		datapoints.append(item_wise_sales_map[key])

# 	return {
# 		"data": {
# 			"labels": labels[:30],  # show max of 30 items in chart
# 			"datasets": [{"name": _("Total Sales Amount"), "values": datapoints[:30]}],
# 		},
# 		"type": "bar",
# 		"fieldtype": "Currency",
# 	}