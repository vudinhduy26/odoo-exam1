from odoo import api, models, fields


class CustomerDiscountCode(models.Model):
    _inherit = "res.partner"

    customer_discount_code = fields.Text(string="Discount Code")
    discount = fields.Float(string="Discount %", compute="cp_discount")
    customer_check = fields.Boolean()

    @api.onchange('customer_discount_code', 'discount', 'customer_check')
    def cp_discount(self):
        for record in self:
            if record.customer_discount_code:
                first = record.customer_discount_code[:4]
                last = record.customer_discount_code[4:]
                if first == "VIP_" and last.isdigit():
                    record.discount = float(last)
                    record.customer_check = True
                else:
                    record.customer_check = False
                    record.discount = 0.00
            else:
                record.customer_check = False
                record.discount = 0.00
