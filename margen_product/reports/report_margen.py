# -*- coding: utf-8 -*-


from odoo import fields, models, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
import base64
import datetime
import xlsxwriter
from io import BytesIO
import io


class ReportMargenSale(models.TransientModel):
    _name = "report.margen.product.sale"
    _description = 'Reporte de margen de productos'
    
    name = fields.Char('Nombre', default='Informe de Margen de Producto', readonly=True)
    date_from = fields.Date('Desde', required=True, default=(fields.Date.today() - relativedelta(month=1)))
    date_to = fields.Date('Hasta', required=True, default=(fields.Date.today()))
    partner_ids = fields.Many2many('res.partner', string='Clientes', copy=False) 
    brand_ids = fields.Many2many('product.brand', string='Marcas')
    xls_file = fields.Binary(string="XLS file")
    xls_filename = fields.Char()
    

    def compute_report(self):
        def _add_where(table, fld, vl):
            return f" AND {table}.{fld} IN ({','.join(str(x.id) for x in vl)})"
        
        cr = self._cr
        wh = ''
        uid = self.env.user.id
        dt_now = fields.Datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt_from = str(self.date_from)
        dt_to = str(self.date_to)
        wh = '' 
        if self.partner_ids:
            wh += _add_where('am', 'partner_id', self.partner_ids)
        if self.brand_ids:
            wh += _add_where('pt', 'product_brand_id', self.brand_ids)

            
        #add_fields_insert, add_fields_select, add_fields_from = self.extended_compute_fields()
            
        cr.execute(f'DELETE FROM margen_report_line_sale')
            
        qry = f'''
                INSERT INTO margen_report_line_sale (invoice_date, invoice_id, partner_id, product_id, default_code, product_brand_id, quantity, price_subtotal, cost, utility, 
                                                percentage_uti, percentage_renta, create_date, write_date)

                SELECT
                    am.invoice_date,
                    aml.move_id,
                    am.partner_id,
                    aml.product_id, 
                    pt.default_code,
                    pt.product_brand_id,
                    aml.quantity * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END) AS num_qty,
                    aml.price_subtotal * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END) AS subtotal,
                    cost_line.cost_product,
                    (aml.price_subtotal * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END) - cost_line.cost_product) AS difference,
                    ((aml.price_subtotal * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END) - cost_line.cost_product) / 
                    NULLIF(aml.price_subtotal * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END),0)) AS utility,
                    ((aml.price_subtotal * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END) - cost_line.cost_product) / 
                    NULLIF(cost_line.cost_product, 0)) AS renta,
                    '{dt_now}', 
                    '{dt_now}'

                FROM 
                    account_move_line aml
                    LEFT JOIN account_move am ON aml.move_id = am.id
                    LEFT JOIN product_product pp ON aml.product_id = pp.id
                    LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
                    LEFT JOIN product_brand pb ON pt.product_brand_id = pb.id
                    LEFT JOIN sale_order so ON am.sale_id = so.id
                    --LEFT JOIN stock_picking sp ON sp.sale_id = so.id
                    --LEFT JOIN stock_move sm ON sp.id = sm.picking_id
                    --LEFT JOIN stock_valuation_layer svl ON sm.id = svl.stock_move_id
                    --LEFT JOIN account_move am2 ON svl.account_move_id = am2.id 
                    --LEFT JOIN account_move_line aml2 ON am2.id = aml2.move_id
                    --LEFT JOIN account_account aa2 ON aml2.account_id = aa2.id 
                    LEFT JOIN (
                            SELECT
                                aml2.product_id AS product_id,
                                aml2.partner_id AS partner_id,
                                CASE 
                                    WHEN aml2.quantity < 0 THEN ABS(aml2.quantity)
                                    ELSE aml2.quantity * (-1)
                                END AS quantity,
                                sp2.sale_id AS sale,
                                SUM(aml2.debit - aml2.credit) AS cost_product
                            FROM
                                stock_valuation_layer svl
                                LEFT JOIN account_move am2 ON svl.account_move_id = am2.id 
                                LEFT JOIN account_move_line aml2 ON am2.id = aml2.move_id
                                LEFT JOIN stock_move sm ON svl.stock_move_id = sm.id
                                LEFT JOIN stock_picking sp2 ON sm.picking_id = sp2.id
                                LEFT JOIN sale_order so ON sp2.sale_id = so.id
                                LEFT JOIN account_account aa2 ON aml2.account_id = aa2.id 
                            WHERE
                                ABS(svl.value) = (aml2.debit - aml2.credit) AND 
                                aa2.code LIKE '61%' AND
                                am2.state = 'posted' AND
                                am2.date BETWEEN '{dt_from}' AND '{dt_to}'
                                
                                
                            GROUP BY
                                aml2.product_id,
                                aml2.partner_id,
                                sp2.sale_id,
                                aml2.quantity
                                
                            
    
                        ) AS cost_line ON pp.id = cost_line.product_id AND am.partner_id = cost_line.partner_id AND cost_line.sale = so.id AND cost_line.quantity = aml.quantity


                    WHERE
                        am.move_type IN ('out_invoice', 'out_refund') AND
                        pt.detailed_type IN ('product', 'service', 'consu') AND
                        am.state = 'posted' AND
                        am.invoice_date BETWEEN   '{dt_from}' AND '{dt_to}' 
                        {wh}
                    --GROUP BY 
                    --    am.invoice_date,
                    --    am.partner_id,
                    --    aml.product_id,
                    --    am.move_type,
                    --    pt.default_code,
                    --    aml2.debit,
                    --    aml2.credit,
                    --    pt.product_brand_id,
                    --    aml.price_subtotal,
                    --    aml.id
                    ORDER BY
                        aml.move_id, 
                        am.invoice_date
                        
                   '''     
        cr.execute(qry)

    def analysis(self):
        self.compute_report()
        view_id = self.env['ir.ui.view'].search([('name','=','margen_product.view_margen_report_line_sale_pivot')])
        return {
                'name': 'Margen de ventas de productos',
                'view_type': 'form',
                'view_mode': 'pivot',
                'view_id': view_id.id, 
                'res_model': 'margen.report.line.sale',
                'type': 'ir.actions.act_window'
            }

    def _compute_excel(self):
        def _add_where(table, fld, vl):
            return f" AND {table}.{fld} IN ({','.join(str(x.id) for x in vl)})"
    
        #APLICAR FILTROS
        wh = '' 
        if self.partner_ids:
            wh += _add_where('am', 'partner_id', self.partner_ids)
        if self.brand_ids:
            wh += _add_where('pt', 'product_brand_id', self.brand_ids)

        cr = self.env.cr
        dt_from = str(self.date_from)
        dt_to = str(self.date_to)
        cr.execute(f'''SELECT
                            am.invoice_date,
                            am.name,
                            rp.name,
                            pt.name, 
                            pt.default_code,
                            pb.name,
                            aml.quantity * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END) AS num_qty,
                            aml.price_subtotal * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END) AS subtotal,
                            cost_line.cost_product,
                            (aml.price_subtotal * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END) - cost_line.cost_product) AS difference,
                            ((aml.price_subtotal * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END) - cost_line.cost_product) / 
                            NULLIF(aml.price_subtotal * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END),0)) AS utility,
                            ((aml.price_subtotal * (CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE -1 END) - cost_line.cost_product) / 
                            NULLIF(cost_line.cost_product, 0)) AS renta
                            
                            

                        FROM account_move_line aml
                            LEFT JOIN account_move am ON aml.move_id = am.id
                            LEFT JOIN product_product pp ON aml.product_id = pp.id
                            LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
                            LEFT JOIN product_brand pb ON pt.product_brand_id = pb.id
                            LEFT JOIN res_partner rp ON am.partner_id = rp.id
                            LEFT JOIN sale_order so ON am.sale_id = so.id
                            LEFT JOIN (
                                    SELECT
                                        aml2.product_id AS product_id,
                                        aml2.partner_id AS partner_id,
                                        CASE 
                                            WHEN aml2.quantity < 0 THEN ABS(aml2.quantity)
                                            ELSE aml2.quantity * (-1)
                                        END AS quantity,
                                        sp2.sale_id AS sale,
                                        SUM(aml2.debit - aml2.credit) AS cost_product
                                    FROM
                                        stock_valuation_layer svl
                                        LEFT JOIN account_move am2 ON svl.account_move_id = am2.id 
                                        LEFT JOIN account_move_line aml2 ON am2.id = aml2.move_id
                                        LEFT JOIN stock_move sm ON svl.stock_move_id = sm.id
                                        LEFT JOIN stock_picking sp2 ON sm.picking_id = sp2.id
                                        LEFT JOIN sale_order so ON sp2.sale_id = so.id
                                        LEFT JOIN account_account aa2 ON aml2.account_id = aa2.id 
                                    WHERE
                                        ABS(svl.value) = (aml2.debit - aml2.credit) AND 
                                        aa2.code LIKE '61%' AND
                                        am2.state = 'posted' AND
                                        am2.date BETWEEN '{dt_from}' AND '{dt_to}'


                                    GROUP BY
                                        aml2.product_id,
                                        aml2.partner_id,
                                        sp2.sale_id,
                                        aml2.quantity

                            
    
                                ) AS cost_line ON pp.id = cost_line.product_id AND am.partner_id = cost_line.partner_id AND cost_line.sale = so.id AND cost_line.quantity = aml.quantity

                        WHERE
                            am.move_type IN ('out_invoice', 'out_refund') AND
                            pt.detailed_type IN ('product', 'consu', 'service') AND
                            am.state = 'posted' AND
                            am.invoice_date BETWEEN   '{dt_from}' AND '{dt_to}' 
                            {wh}
                            
                        ORDER BY
                        am.name, 
                        am.invoice_date
                        
                      ''')
        result = cr.fetchall()
        return result
        
    def get_xlsx_report(self):
        result = self._compute_excel()
        output = io.BytesIO()
        titles = [
                'Fecha',
                'Factura',
                'Nombre Cliente',
                'Producto', 
                'Referencia Interna',
                'Marca',
                'Cantidad',
                'Ingreso', 
                'Costo',
                'Utilidad', 
                '%Rentabilidad', 
                '%Utilidad'
                ]
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet()

         # Formants
        title_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#87CEEB',
            'font_color': 'black',
            'font_size': 12,
        })
    
        user_format = workbook.add_format({
            'bold': True,
            'font_color': 'black',
        })
        
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

        worksheet.set_column("A:P", 15)
        worksheet.set_row(0, 30)

        # Write title with merged cells
        worksheet.merge_range('A1:P1', 'REPORTE DE MARGEN DE VENTAS DE PRODUCTOS', title_format)

        # Write Generador and Usuario
        worksheet.write('A2', 'Generador:', user_format)
        worksheet.write('B2', self.env.user.name)


        start_date = self.date_from
        end_date = self.date_to
        date_range = f'Fecha Inicio: {start_date} - Fecha Fin: {end_date}'
        worksheet.write('A3', date_range, user_format)

        # Write headers
        for col_num, title in enumerate(titles):
            worksheet.write(5, col_num, title, title_format)
        
    
        money_format = workbook.add_format({'num_format': '$#,##0.00'})
        for index, data in enumerate(result):
            row = index + 6
            for col_num, d in enumerate(data):
                if isinstance(d, datetime.date):
                    worksheet.write_datetime(row, col_num, d, date_format)
                elif col_num in [7,8, 9]:
                    worksheet.write(row, col_num, d, money_format)
                else:
                    worksheet.write(row, col_num, d)

        
        workbook.close()
        xlsx_data = output.getvalue()

        self.xls_file = base64.encodebytes(xlsx_data)
        self.xls_filename = "report_margen.xlsx"

class InvoiceReportLineSale(models.TransientModel):
    _name = "margen.report.line.sale"
    _description = "Lineas de reporte de Margen de productos"
    

    product_id = fields.Many2one('product.product', string='Producto', readonly=True)
    invoice_date = fields.Date(readonly=True, string="Fecha de Factura", copy=False, index=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', readonly=True)
    invoice_id = fields.Many2one('account.move', string="Factura", copy=False, readonly=True)
    quantity = fields.Float(string='Cantidad Facturada', readonly=True)
    cost = fields.Float(string='Costo', readonly=True)
    utility = fields.Float(string='Utilidad', readonly=True)
    percentage_uti = fields.Float(string='%Rentabilidad', digits=(1,2), readonly=True)
    percentage_renta = fields.Float(string='%Utilidad', digits=(1,2), readonly=True)
    price_subtotal = fields.Float(string='V. antes Impuesto', readonly=True)
    default_code = fields.Char('Referencia interna', readonly=True)
    product_brand_id = fields.Many2one('product.brand', string="Marca", readonly=True)
    product_type = fields.Selection([
        ('product', 'Almacenable'),
        ('service', 'Servicio'),
        ('consu', 'Consumible'),
        ], string='Tipo de producto', readonly=True)
    
    
    