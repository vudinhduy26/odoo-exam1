# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerDiscountCode(http.Controller):
#     @http.route('/customer_discount_code/customer_discount_code/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_discount_code/customer_discount_code/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_discount_code.listing', {
#             'root': '/customer_discount_code/customer_discount_code',
#             'objects': http.request.env['customer_discount_code.customer_discount_code'].search([]),
#         })

#     @http.route('/customer_discount_code/customer_discount_code/objects/<model("customer_discount_code.customer_discount_code"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_discount_code.object', {
#             'object': obj
#         })
