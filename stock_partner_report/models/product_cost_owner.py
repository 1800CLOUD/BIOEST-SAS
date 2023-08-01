# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductCostOwner(models.Model):
    _name = 'product.cost.owner'
    _description = 'Costo de producto por propietario'

    product_tmpl_id = fields.Many2one('product.template',
                                      'Producto')
    partner_id = fields.Many2one('res.partner',
                                 'Propietario')
    value = fields.Monetary('Valor',
                            currency_field='currency_id',
                            group_expand='avg',)
    currency_id = fields.Many2one('res.currency',
                                  'Moneda',
                                  default=lambda self: self.env.company.currency_id)
    qty = fields.Float('Cantidad',
                       default=1)
    uom_id = fields.Many2one('uom.uom',
                             'Unidad de Medida')
    product_uom_id = fields.Many2one('uom.uom',
                                     'UdM del producto',
                                     related='product_tmpl_id.uom_id')
    product_uom_category_id = fields.Many2one('uom.category',
                                     'Categoria de UdM del producto',
                                     related='product_tmpl_id.uom_id.category_id')
    
    def get_value(self, partner_id=False, product_id=False, uom_q_id=False):
        uom_obj = self.env['uom.uom']
        msg = ''
        if not partner_id:
            msg += '\n- Propietario'
        if not product_id:
            msg = '\n- Producto'
        if not uom_q_id:
            msg = '\n- Unidad de medida'
        if msg:
            return 'El Cant #%s no tiene los siguientes datos para calcular el costo por propietario: \n' + msg
        record = self.search([('partner_id', '=', partner_id),
                              ('product_tmpl_id', '=', product_id)],
                              order='id desc',
                              limit=1)
        result_value = 0
        if record:
            uom_id = record.uom_id
            qty = record.qty
            value = record.value
            uom_des_id = uom_obj.browse(uom_q_id)
            qty_dest = uom_id._compute_quantity(qty, uom_des_id)
            result_value = value/qty_dest
        return result_value
    
    @api.onchange('product_tmpl_id')
    def onchange_product_tmpl_id(self):
        if self.product_tmpl_id:
            self.uom_id = self.product_tmpl_id.uom_id.id or False
        else:
            self.uom_id = False
