from odoo import models, fields

move_types = {
    '1': 'Entrada',
    '-1': 'Salida',
    '0': 'Interna',
}
class StockMoveWizard(models.TransientModel):
    _inherit = 'stock.move.wizard'


    def prepare_data(self):
        self.ensure_one()

        Product = self.env['product.product']
        Move = self.env['stock.move']

        products = self.products_ids
        if not products:
            domain = [
                ('type', '=', 'product'),
                '|',
                ('company_id', '=', self.company_id.id),
                ('company_id', '=', False)
            ]
            products = Product.search(domain)

        product_data = []
        for product in products:
            move_data = []
            move_domain = [
                ('date', '>=', fields.Datetime.to_datetime(self.date_start)),
                ('date', '<=', fields.Datetime.to_datetime(self.date_end)),
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('company_id', '=', self.company_id.id)
            ]
            moves = Move.search(move_domain)
            svl_date = fields.Date.subtract(self.date_start, days=1)
            svl_quantity = product.with_context(to_date=svl_date).quantity_svl
            for move in moves:
                # Type
                if move._is_in():
                    move_type = 1
                elif move._is_out():
                    move_type = -1
                else:
                    move_type = 0

                # Qty
                qty = move.product_uom_qty * move_type

                # Price
                if move_type == 1:
                    price_unit = self._get_in_price_unit(move)
                else:
                    price_unit = move._get_price_unit()
                price_total = price_unit * qty

                move_vals = {
                    'id': move.id,
                    'date': move.date,
                    'reference': move.reference,
                    'description_move': move.description_move,
                    'product': move.product_id.display_name,
                    'from': move.location_id.complete_name,
                    'to': move.location_dest_id.complete_name,
                    'type': move_types.get(str(move_type)),
                    'init': svl_quantity,
                    'demand': move.product_uom_qty,
                    'final': svl_quantity + qty,
                    'uom': move.product_uom.name,
                    'unit': price_unit,
                    'total': price_total,
                    'company': move.company_id.name,
                    'status': move.state,
                }
                move_data.append(move_vals)
                svl_quantity += qty

            product_vals = {
                'id': product.id,
                'name': product.display_name,
                'moves': move_data,
            }
            if not move_data:
                continue
            product_data.append(product_vals)

        return {
            'company': self.company_id.name,
            'user': self.env.user.name,
            'start': self.date_start,
            'end': self.date_end,
            'products': product_data
        }

    def report_data(self):
        return self.prepare_data()