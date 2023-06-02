# -*- coding: utf-8 -*-
# from odoo import http


# class L10nCoExtended(http.Controller):
#     @http.route('/l10n_co_extended/l10n_co_extended', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_co_extended/l10n_co_extended/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_co_extended.listing', {
#             'root': '/l10n_co_extended/l10n_co_extended',
#             'objects': http.request.env['l10n_co_extended.l10n_co_extended'].search([]),
#         })

#     @http.route('/l10n_co_extended/l10n_co_extended/objects/<model("l10n_co_extended.l10n_co_extended"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_co_extended.object', {
#             'object': obj
#         })
