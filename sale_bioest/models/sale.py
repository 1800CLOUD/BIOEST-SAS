# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_cancel(self):
        order = self.invoice_ids.filtered(lambda order: order.state == 'posted')
        if order:
            raise ValidationError('No es posible Cancelar esta orden de venta, contiene facturas en estado "Publicado"')
        res = super(SaleOrder, self).action_cancel()
        return res

    def action_confirm(self):
        if not self.env.user.has_group('sale_bioest.group_manager_sales_bi'):
            raise ValidationError('No esta autorizado para confirmar pedidos de venta, por favor contacte a soporte si cree que deberia tener el permiso')
        res = super(SaleOrder, self).action_confirm()
        return res

    