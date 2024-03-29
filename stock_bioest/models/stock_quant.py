# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

from odoo.tools.float_utils import float_compare, float_is_zero


class StockQuant(models.Model):
    _inherit = 'stock.quant'


    description = fields.Text('Motivo del movimiento', copy=False)

    @api.model
    def _get_inventory_fields_create(self):
        allowed_fields = super(StockQuant, self)._get_inventory_fields_create()
        allowed_fields.append('description')
        return allowed_fields
    
    @api.model
    def _get_inventory_fields_write(self):
        fields = super(StockQuant, self)._get_inventory_fields_write()
        fields.append('description')
        return fields 

    def _get_inventory_move_values(self, qty, location_id, location_dest_id, out=False):
        self.ensure_one()
        if fields.Float.is_zero(qty, 0, precision_rounding=self.product_uom_id.rounding):
            name = _('Product Quantity Confirmed')
        else:
            name = _('Product Quantity Updated')
        return {
            'name': self.env.context.get('inventory_name') or name,
            'product_id': self.product_id.id,
            'product_uom': self.product_uom_id.id,
            'product_uom_qty': qty,
            'company_id': self.company_id.id or self.env.company.id,
            'state': 'confirmed',
            'location_id': location_id.id,
            'location_dest_id': location_dest_id.id,
            'is_inventory': True,
            'description_move': self.description,
            'move_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'product_uom_id': self.product_uom_id.id,
                'qty_done': qty,
                'location_id': location_id.id,
                'location_dest_id': location_dest_id.id,
                'company_id': self.company_id.id or self.env.company.id,
                'lot_id': self.lot_id.id,
                'package_id': out and self.package_id.id or False,
                'result_package_id': (not out) and self.package_id.id or False,
                'owner_id': self.owner_id.id,
            })]
        }
    
    
