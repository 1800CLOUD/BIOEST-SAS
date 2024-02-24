# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _prepare_line(self, order_line):
        res = super(PosSession, self)._prepare_line(order_line)
        res['income_account_id'] = self.get_income_account_ext(order_line).id
        return res

    def get_income_account_ext(self, order_line):
        product = order_line.product_id
        acc_type = order_line.price_subtotal < 0 and 'refund' or 'income'
        income_account = product.with_company(order_line.company_id)._get_product_accounts()[acc_type] or self.config_id.journal_id.default_account_id
        if not income_account:
            
            raise UserError(_('Por favor, defina una cuenta de %s para este producto: "%s" (id:%d).')
                            % (acc_type == 'income' and 'ingresos' or 'devoluciones',
                               product.name, 
                               product.id))
        return order_line.order_id.fiscal_position_id.map_account(income_account)
