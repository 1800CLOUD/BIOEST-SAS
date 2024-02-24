# -*- coding: utf-8 -*-
from odoo import models, fields, _

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _should_auto_confirm_procurement_mo(self, p):
        res = super(StockRule, self)._should_auto_confirm_procurement_mo(p)
        return (not p.company_id.no_auto_confirm_procurement_mo and (
                (not p.orderpoint_id and p.move_raw_ids) or \
                (p.move_dest_ids.procure_method != 'make_to_order' and not p.move_raw_ids and not p.workorder_ids))
            )
