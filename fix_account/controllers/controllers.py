# -*- coding: utf-8 -*-
# from odoo import http


# class FixAccount(http.Controller):
#     @http.route('/fix_account/fix_account', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fix_account/fix_account/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fix_account.listing', {
#             'root': '/fix_account/fix_account',
#             'objects': http.request.env['fix_account.fix_account'].search([]),
#         })

#     @http.route('/fix_account/fix_account/objects/<model("fix_account.fix_account"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fix_account.object', {
#             'object': obj
#         })
