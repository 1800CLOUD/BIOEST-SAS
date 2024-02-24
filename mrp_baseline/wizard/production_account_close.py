# -*- coding: utf-8 -*-

from odoo import _, fields, models
from odoo.exceptions import ValidationError


ACCOUNT_DOMAIN = "['&', '&', '&', ('deprecated', '=', False), ('internal_type', '=', 'other'), ('company_id', '=', company_id), ('is_off_balance', '=', False)]"


class ProductionAccountClose(models.TransientModel):
    _name = 'production.account.close'
    _description = 'Close Production Accounts'

    accounts_ids = fields.Many2many(
        comodel_name='account.account',
        domain=ACCOUNT_DOMAIN
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company
    )

    date_begin = fields.Date()
    date_end = fields.Date()

    line_ids = fields.One2many(
        comodel_name='production.account.close.line',
        inverse_name='close_id'
    )

    def query_get(self):
        return """
            select 
                account_id as account_id, 
                product_id as product_id, 
                sum(debit) as debit, 
                sum(credit) as credit 
            from 
                account_move_line 
            where 
                parent_state = 'posted' 
                and company_id = %s 
                and account_id = %s 
                and date between '%s' and '%s' 
                and product_id is not null 
            group by 
                account_id, 
                product_id
        """

    def query_get_account(self, account):
        query_get = self.query_get()
        query = query_get % (
            self.env.company.id,
            account.id,
            fields.Date.to_string(self.date_begin),
            fields.Date.to_string(self.date_end)
        )
        self._cr.execute(query)
        return self._cr.dictfetchall()

    def action_return(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Close Production Accounts'),
            'res_model': 'production.account.close',
            # 'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
        }

    def action_calculate(self):
        self.write({'line_ids': [(2, line.id, 0) for line in self.line_ids]})

        line_ids = []
        for account in self.accounts_ids:
            products = self.query_get_account(account)
            for product in products:
                debit = product.get('debit')
                credit = product.get('credit')
                residual = debit - credit
                vals = {
                    'account_id': account.id,
                    'product_id': product.get('product_id'),
                    'debit': debit,
                    'credit': credit,
                    'residual': residual
                }
            line_ids.append((0, 0, vals))

        self.write({'line_ids': line_ids})

        return self.action_return()

    def action_confirm(self):
        for line in self.line_ids:
            if not line.residual:
                continue

            product = line.product_id
            if product.type != 'product':
                verror = _('Product %s is not storable.')
                raise ValidationError(verror % product.display_name)

            # TO DO
            # product.cost_method

            price = product.standard_price
            qty = product.qty_available
            if not qty:
                verror = _(
                    'Product %s has no quantity. You must do the adjustment manually.'
                )
                raise ValidationError(verror % product.display_name)

            # Calculate
            standard = (line.residual / qty) + price
            product_id = product.with_context(
                default_date=self.date_end,
                default_expense=line.account_id
            )
            product_id.write({'standard_price': standard})
        return self.action_calculate()


class ProductionAccountCloseLine(models.TransientModel):
    _name = 'production.account.close.line'
    _description = 'Close Production Accounts Lines'

    account_id = fields.Many2one('account.account')

    close_id = fields.Many2one('production.account.close')

    credit = fields.Monetary()

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id
    )

    debit = fields.Monetary()

    product_id = fields.Many2one('product.product')

    residual = fields.Monetary()
