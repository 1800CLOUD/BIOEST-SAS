# -*- coding: utf-8 -*-

from odoo import fields, models, _


class StockMoveWizard(models.TransientModel):
    _inherit = 'stock.move.wizard'

    def _get_move_vals(self, move, product, initial_qty):
        vals = super(
            StockMoveWizard, self)._get_move_vals(move, product, initial_qty)
        if self.owner_id:
            pco_obj = self.env['product.cost.owner']
            price_unit = pco_obj.get_value(
                partner_id=self.owner_id.id,
                product_id=product.product_tmpl_id.id,
                uom_q_id=move.product_uom.id)
            price_total = price_unit * vals.get('qty', 0)
            vals.update({
                'unit': price_unit,
                'total': price_total,
            })
        return vals
