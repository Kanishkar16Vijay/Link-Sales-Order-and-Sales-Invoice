import frappe

@frappe.whitelist()
def link_so_si(sales_order, sales_invoice, link_name) :

    so = frappe.get_doc("Sales Order", sales_order)
    si = frappe.get_doc("Sales Invoice", sales_invoice)
    flag = True

    if len(so.items) == len(si.items) and so.grand_total == si.grand_total :
        for item1, item2 in zip(so.items, si.items) :
            if item1.item_code != item2.item_code or item1.qty != item2.qty :
                flag = False
                break

        if flag :
            for item1, item2 in zip(so.items, si.items) :
                    frappe.db.set_value("Sales Invoice Item", item2.name, "sales_order", so.name)
                    frappe.db.set_value("Sales Invoice Item", item2.name, "so_detail", item1.name)
            frappe.db.set_value("Sales Order Invoice Link Request", link_name, "status", "Approved")
            frappe.db.set_value("Sales Order Invoice Link Request", link_name, "approved_by", frappe.session.user)

            frappe.msgprint("Sales Order and Sales Invoice Linked Successfully")
        else :
            frappe.db.set_value("Sales Order Invoice Link Request", link_name, "status", "Rejected")
            frappe.db.set_value("Sales Order Invoice Link Request", link_name, "approved_by", frappe.session.user)
            frappe.db.set_value("Sales Order Invoice Link Request", link_name, "reason", "Item details does not match with sales order")

            frappe.msgprint("Sales Order and Sales Invoice Item details or Grand Total does not match")
    else :
        frappe.db.set_value("Sales Order Invoice Link Request", link_name, "status", "Rejected")
        frappe.db.set_value("Sales Order Invoice Link Request", link_name, "approved_by", frappe.session.user)
        frappe.db.set_value("Sales Order Invoice Link Request", link_name, "reason", "Item details does not match with sales order")

        frappe.msgprint("Sales Order and Sales Invoice Item details or Grand Total does not match")