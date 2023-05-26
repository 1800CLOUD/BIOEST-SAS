# -*- coding: utf-8 -*-
# from odoo import http


# class StockBioest(http.Controller):
#     @http.route('/stock_bioest/stock_bioest', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_bioest/stock_bioest/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_bioest.listing', {
#             'root': '/stock_bioest/stock_bioest',
#             'objects': http.request.env['stock_bioest.stock_bioest'].search([]),
#         })

#     @http.route('/stock_bioest/stock_bioest/objects/<model("stock_bioest.stock_bioest"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_bioest.object', {
#             'object': obj
#         })
