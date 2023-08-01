# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    owner_val_unit = fields.Monetary('Valor unitario', 
                                     compute='_compute_owner_val_init',
                                     help='Valor unitario por propietario')
    owner_val_total = fields.Monetary('Valor total', 
                                      compute='_compute_owner_val_total',
                                      help='Valor Total por propietario')

    @api.depends('owner_id', 'product_id', 'currency_id')
    def _compute_owner_val_init(self):
        cost_owner_obj = self.env['product.cost.owner']
        for record in self:
            if record.owner_id:
                val_unit = cost_owner_obj.get_value(
                    record.owner_id.id,
                    record.product_id.product_tmpl_id.id,
                    record.product_uom_id.id
                )
                record.owner_val_unit = val_unit
            else:
                record.owner_val_unit = 0
    
    @api.depends('owner_id', 'product_id', 'quantity')
    def _compute_owner_val_total(self):
        for record in self:
            record.owner_val_total = record.quantity * record.owner_val_unit
    
    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """ This override is done in order for the grouped list view to display the total value of
        the quants inside a location. This doesn't work out of the box because `value` is a computed
        field.
        """
        if 'owner_val_unit' not in fields and 'owner_val_total' not in fields:
            return super(StockQuant, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        res = super(StockQuant, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        for group in res:
            if group.get('__domain'):
                quants = self.search(group['__domain'])
                group['owner_val_unit'] = sum(quant.owner_val_unit for quant in quants)/len(quants)
                group['owner_val_total'] = sum(quant.owner_val_total for quant in quants)
        return res
    
    def _get_action_stock_partner_report(self):
        action_rec = self.with_context(search_default_internal_loc=1,
                                       search_default_productgroup=1,
                                       search_default_locationgroup=1,).action_view_quants()
        action_rec['domain'] = [('owner_id', '!=', False)]
        action_rec['name'] = 'Existencias a la Mano por Tercero'
        action_rec['view_id'] = self.env.ref('stock_partner_report.stock_quant_owner_tree_editable_view').id
        views = []
        for view in action_rec['views']:
            if view[1] == 'list':
                views.append((action_rec['view_id'], 'list'))
            else:
                views.append(view)
        action_rec['views'] = views
        return action_rec
