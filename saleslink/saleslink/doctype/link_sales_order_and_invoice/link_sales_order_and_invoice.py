# Copyright (c) 2025, Kanishkar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LinkSalesOrderandInvoice(Document):
    def before_save(self) :
        self.set("unlinked_sales_order", [])
        self.set("unlinked_sales_invoice", [])

        sales_order = frappe.get_all("Sales Order", filters={"customer" : self.customer})
        sales_invoice = frappe.get_all("Sales Invoice", filters={"customer": self.customer})

        for invoice in sales_invoice :
            si = frappe.get_doc("Sales Invoice", invoice.name)
            if not si.items[0].sales_order :
                self.append("unlinked_sales_invoice", {
                    "sales_invoice": si.name,
                    "date": si.posting_date,
                    "amount": si.grand_total,
                    "status": si.status
				})
            else :
                for so in sales_order :
                    if so.name == si.items[0].sales_order :
                        so.name = ''

        for order in sales_order :
            if order.name :
                so = frappe.get_doc("Sales Order", order.name)
                self.append("unlinked_sales_order",{
                    "sales_order" : so.name,
                    "date" : so.transaction_date,
                    "amount" : so.grand_total,
                    "status" : so.status
				})