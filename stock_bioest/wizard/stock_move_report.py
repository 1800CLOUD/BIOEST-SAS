from odoo import models, fields

move_types = {
    '1': 'Entrada',
    '-1': 'Salida',
    '0': 'Interna',
}
class StockMoveWizard(models.TransientModel):
    _inherit = 'stock.move.wizard'

    def _get_move_vals(self, move, product, initial_qty):
        vals = super(StockMoveWizard, self)._get_move_vals(move, product, initial_qty)
        vals['description_move'] = move.description_move
        return vals