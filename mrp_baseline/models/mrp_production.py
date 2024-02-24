# -*- coding: utf-8 -*-

from odoo import models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    ## SE COMENTA PORQUE HACE DOBLE AFECTACION AL COSTO UNITARIO DE LOS PRODUCTOS
    # def _cal_price(self, consumed_moves):
    #     res = super(MrpProduction, self)._cal_price(consumed_moves)
    #     finished_move = self.move_finished_ids.filtered(
    #         lambda x: x.product_id == self.product_id and x.state not in ('done', 'cancel') and x.quantity_done > 0
    #     )
    #     if finished_move:
    #         work_orders = self.workorder_ids.filtered(
    #             lambda w: w.workcenter_id.workcenter_cost
    #         )
    #         for work_order in work_orders:
    #             work_order.action_cost()
    #     return res
