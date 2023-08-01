# -*- coding: utf-8 -*-
# from odoo import http


# class StockPartnerReport(http.Controller):
#     @http.route('/stock_partner_report/stock_partner_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_partner_report/stock_partner_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_partner_report.listing', {
#             'root': '/stock_partner_report/stock_partner_report',
#             'objects': http.request.env['stock_partner_report.stock_partner_report'].search([]),
#         })

#     @http.route('/stock_partner_report/stock_partner_report/objects/<model("stock_partner_report.stock_partner_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_partner_report.object', {
#             'object': obj
#         })
