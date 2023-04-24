# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    
    def action_assign(self):
        for production in self:
            location_dest_id = production.move_raw_ids.location_id
            product_qty_available = sum(location_dest_id.quant_ids.filtered(lambda q: q.product_id == production.product_id).mapped('quantity'))
            if product_qty_available >= production.product_uom_qty:
                production.move_raw_ids._action_assign()
            else:
                raise UserError(_('No hay suficiente cantidad disponible en la ubicación seleccionada.'))
        return True
