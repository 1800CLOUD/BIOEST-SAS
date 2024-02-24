# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    no_auto_confirm_procurement_mo = fields.Boolean(
        related='company_id.no_auto_confirm_procurement_mo',
        readonly=False
    )