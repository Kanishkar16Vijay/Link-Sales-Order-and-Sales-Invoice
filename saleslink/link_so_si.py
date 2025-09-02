import frappe

@frappe.whitelist()
def link_so_si(docname, sales_order, sales_invoice) :
    sales_order = sales_order[2:-2]
    sales_invoice = sales_invoice[2:-2]
    so = frappe.get_doc("Sales Order", sales_order)
    si = frappe.get_doc("Sales Invoice", sales_invoice)
    for itm1,itm2 in zip(so.items, si.items) :
        if itm1.item_code == itm2.item_code and itm1.qty == itm2.qty and itm1.rate == itm2.rate :
            frappe.db.set_value("Sales Invoice Item", itm2.name, "sales_order", so.name)
            frappe.db.set_value("Sales Invoice Item", itm2.name, "so_detail", itm1.name)
            # frappe.db.commit()
            frappe.msgprint("Sales Order linked to Sales Invoice")
        else :
            frappe.msgprint("Item details does not match")