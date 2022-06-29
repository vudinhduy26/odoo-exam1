from odoo import fields, models, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    discount_of_customer = fields.Text(string="Discount Customer", related="partner_id.customer_discount_code")
    discount_vip = fields.Float(string="Discount %", related='partner_id.discount')


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('discount', 'order_id.discount_vip', 'product_id.discount_product')
    def change_discount_filed(self):
        for record in self:
            if record.order_id.discount_vip != 0.00:
                record.discount = record.order_id.discount_vip

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        res = super(SaleOrderLineInherit, self)._compute_amount()
        for line in self:
            line.discount = line.order_id.discount_vip
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                    'account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
        return res