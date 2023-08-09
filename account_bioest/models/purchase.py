# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    
    def action_create_invoice(self):
        
        if len(self) >= 2:
            raise UserError(_('No puede seleccionar 2 o mas ordenes de compra para crear facturas de proveedor.'))

        
        return super(PurchaseOrder, self).action_create_invoice()