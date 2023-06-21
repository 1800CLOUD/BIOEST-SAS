# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_cancel(self):
        order = self.invoice_ids.filtered(lambda order: order.state == 'posted')
        if order:
            raise ValidationError('No es posible Cancelar esta orden de venta, contiene facturas en estado "Publicado"')
        res = super(SaleOrder, self).action_sale()
        return res
