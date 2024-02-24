# -*- coding: utf-8 -*-
# from odoo import http


# class PointOfSaleBaseline(http.Controller):
#     @http.route('/point_of_sale_baseline/point_of_sale_baseline', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/point_of_sale_baseline/point_of_sale_baseline/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('point_of_sale_baseline.listing', {
#             'root': '/point_of_sale_baseline/point_of_sale_baseline',
#             'objects': http.request.env['point_of_sale_baseline.point_of_sale_baseline'].search([]),
#         })

#     @http.route('/point_of_sale_baseline/point_of_sale_baseline/objects/<model("point_of_sale_baseline.point_of_sale_baseline"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('point_of_sale_baseline.object', {
#             'object': obj
#         })
