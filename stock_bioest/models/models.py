# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class stock_bioest(models.Model):
#     _name = 'stock_bioest.stock_bioest'
#     _description = 'stock_bioest.stock_bioest'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
