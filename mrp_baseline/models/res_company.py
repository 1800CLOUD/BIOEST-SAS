# -*- coding: utf-8 -*-
from odoo import fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    no_auto_confirm_procurement_mo = fields.Boolean(
        'Quitar confirmación automática en reglas de inventario',
        help='No se confirmarán automáticamente las ordenes de producción creadas por las rutas de inventario.'
    )