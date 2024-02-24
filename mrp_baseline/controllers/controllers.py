# -*- coding: utf-8 -*-
# from odoo import http


# class MrpBaseline(http.Controller):
#     @http.route('/mrp_baseline/mrp_baseline', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_baseline/mrp_baseline/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_baseline.listing', {
#             'root': '/mrp_baseline/mrp_baseline',
#             'objects': http.request.env['mrp_baseline.mrp_baseline'].search([]),
#         })

#     @http.route('/mrp_baseline/mrp_baseline/objects/<model("mrp_baseline.mrp_baseline"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_baseline.object', {
#             'object': obj
#         })
