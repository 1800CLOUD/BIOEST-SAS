# -*- coding: utf-8 -*-

from odoo import _, fields, models
from odoo.exceptions import UserError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    wc_account_move_id = fields.Many2one(
        comodel_name='account.move',
        string='Journal Entry',
        copy=False
    )

    def action_cost(self):
        self.ensure_one()
        workcenter = self.workcenter_id
        if not workcenter or not workcenter.workcenter_cost:
            return False

        move = self.create_account_move()
        if not move:
            return False

        return self.write({'wc_account_move_id': move.id})

    def create_account_move(self):
        self.ensure_one()
        Move = self.env['account.move']
        move_vals = self.prepare_account_move()
        if not move_vals:
            return False

        move = Move.create(move_vals)
        move.action_post()
        return move

    def prepare_account_move(self):
        self.ensure_one()
        journal = self.workcenter_id.stock_journal_id
        if not journal:
            raise UserError(
                _("You don't have stock journal defined on your work center.")
            )

        line_ids = self.prepare_account_move_line()
        if not line_ids:
            return False

        return {
            'journal_id': journal.id,
            'line_ids': line_ids,
            'date': fields.Date.today(),
            'ref': _("[WC] %s", self.display_name),
            'move_type': 'entry',
        }

    def prepare_account_move_line(self):
        self.ensure_one()

        display_name = _("[WC] %s", self.display_name)
        partner = self.env.company.partner_id
        product = self.production_id.product_id
        workcenter = self.workcenter_id

        time_lines = self.time_ids.filtered(
            lambda t: t.date_end and t.cost_already_recorded
        )
        duration = sum(time_lines.mapped('duration'))
        wc_cost = (duration / 60.0) * workcenter.costs_hour
        cost = self.company_id.currency_id.round(wc_cost)

        accounts_data = product.product_tmpl_id.get_product_accounts()
        acc_valuation = accounts_data.get('stock_valuation', False)
        if not acc_valuation:
            return False

        credit_account_id = workcenter.account_expense_id
        if not credit_account_id:
            raise UserError(
                _("You don't have expense account defined on your work center.")
            )

        debit_line_vals = {
            'name': display_name,
            'product_id': product.id,
            'product_uom_id': product.uom_id.id,
            'partner_id': partner.id,
            'debit': cost,
            'credit': 0,
            'account_id': acc_valuation.id,
        }

        credit_line_vals = {
            'name': display_name,
            'product_id': product.id,
            'product_uom_id': product.uom_id.id,
            'partner_id': partner.id,
            'debit': 0,
            'credit': cost,
            'account_id': credit_account_id.id,
        }

        if self.wc_analytic_account_line_id:
            credit_line_vals.update({
                'analytic_account_id': self.wc_analytic_account_line_id.id,
                'analytic_line_ids': [(4, self.wc_analytic_account_line_id.id, 0)]
            })

        return [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
