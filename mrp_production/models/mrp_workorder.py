# -*- coding: utf-8 -*-

from odoo import models, api, tools,  _
from odoo.exceptions import UserError

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    @api.depends('time_ids.duration', 'qty_produced')
    def _compute_duration(self):
        for order in self:
            order.duration = order.duration_expected
            order.duration_unit = round(order.duration / max(order.qty_produced, 1), 2)  # rounding 2 because it is a time
            if order.duration_expected:
                order.duration_percent = 100 * (order.duration_expected - order.duration) / order.duration_expected
            else:
                order.duration_percent = 0
    

        #return super(UoM, self)._compute_quantity(qty, to_unit, round=round, rounding_method=rounding_method, raise_if_failure=raise_if_failure)
