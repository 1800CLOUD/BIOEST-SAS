# -*- coding: utf-8 -*-

from odoo import models, api, tools,  _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'uom.uom'

    
    def _compute_quantity(self, qty, to_unit, round=True, rounding_method='UP', raise_if_failure=True):
        """ Convert the given quantity from the current UoM `self` into a given one
            :param qty: the quantity to convert
            :param to_unit: the destination UoM record (uom.uom)
            :param raise_if_failure: only if the conversion is not possible
                - if true, raise an exception if the conversion is not possible (different UoM category),
                - otherwise, return the initial quantity
        """
        if not self or not qty:
            return qty
        self.ensure_one()

        if self.category_id.id != to_unit.category_id.id:
            if raise_if_failure:
                raise UserError(_(f'La unidad de medida {self.name} definida en las lineas pertenece a la '
                                f'misma categoría que la unidad de medida {to_unit.name} definida en el producto. '
                                f'Por favor, corrija la unidad de medida definida en la línea de pedido o en el '
                                f'producto, deben pertenecer a la misma categoría.'))
            else:
                return qty

        if self == to_unit:
            amount = qty
        else:
            amount = qty / self.factor
            if to_unit:
                amount = amount * to_unit.factor

        if to_unit and round:
            amount = tools.float_round(amount, precision_rounding=to_unit.rounding, rounding_method=rounding_method)

        return super()._compute_quantity(qty, to_unit, round=round, rounding_method=rounding_method, raise_if_failure=raise_if_failure)
