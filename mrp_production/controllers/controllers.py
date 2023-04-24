# -*- coding: utf-8 -*-
# from odoo import http


# class AccountBioest(http.Controller):
#     @http.route('/account_bioest/account_bioest', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_bioest/account_bioest/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_bioest.listing', {
#             'root': '/account_bioest/account_bioest',
#             'objects': http.request.env['account_bioest.account_bioest'].search([]),
#         })

#     @http.route('/account_bioest/account_bioest/objects/<model("account_bioest.account_bioest"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_bioest.object', {
#             'object': obj
#         })
