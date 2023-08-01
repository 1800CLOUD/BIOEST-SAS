# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cost_owner_id = fields.One2many('product.cost.owner',
                                    'product_tmpl_id',
                                    'Costo por propietario')