# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"


    cost_manufacturing = fields.Float('Costo Tercero', store=True, digits='Stock Weight')
    partner_property = fields.Many2one('res.partner', 'Propietario', store=True)