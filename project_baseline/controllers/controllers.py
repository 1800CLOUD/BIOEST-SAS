# -*- coding: utf-8 -*-
# from odoo import http


# class HelpdeskBaseline(http.Controller):
#     @http.route('/helpdesk_baseline/helpdesk_baseline', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_baseline/helpdesk_baseline/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_baseline.listing', {
#             'root': '/helpdesk_baseline/helpdesk_baseline',
#             'objects': http.request.env['helpdesk_baseline.helpdesk_baseline'].search([]),
#         })

#     @http.route('/helpdesk_baseline/helpdesk_baseline/objects/<model("helpdesk_baseline.helpdesk_baseline"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_baseline.object', {
#             'object': obj
#         })
