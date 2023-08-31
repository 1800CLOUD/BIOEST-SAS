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
    group_by_month = fields.Boolean('Por mes',
                                    help='Agrupa los resultados por mes, cliente y producto')
    

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
                INSERT INTO margen_report_line_sale (
                    invoice_date, invoice_id, partner_id, product_id,
                    default_code, product_brand_id, quantity, price_subtotal,
                    cost, utility, percentage_uti, percentage_renta,
                    create_date, write_date)

                SELECT
                    am.invoice_date AS fecha,
                    am.id           AS factura,
                    rp.id           AS cliente,
                    pp.id           AS producto,
                    pt.default_code AS product_ref,
                    pb.id           AS marca,
                    aml.quantity * (CASE WHEN am.move_type = 'out_invoice' THEN 1 
                                    ELSE -1 END)            AS cantidad,
                    aml.amount_currency*-1                  AS ingreso,
                    svl.value*-1    AS costo,
                    (aml.amount_currency - svl.value)*-1    AS utilidad,
                    (aml.amount_currency - svl.value) /
                    NULLIF(aml.amount_currency, 0)          AS p_utilidad,
                    (aml.amount_currency - svl.value) / 
                    NULLIF(svl.value, 0)                    AS p_rentabilidad,
                    '{dt_now}', 
                    '{dt_now}'

                FROM account_move_line AS aml
                LEFT JOIN account_move      AS am ON am.id = aml.move_id
                LEFT JOIN res_partner       AS rp ON rp.id = am.partner_id
                LEFT JOIN product_product   AS pp ON pp.id = aml.product_id
                LEFT JOIN product_template  AS pt ON pt.id = pp.product_tmpl_id
                LEFT JOIN product_brand     AS pb ON pb.id = pt.product_brand_id
                LEFT JOIN sale_order_line_invoice_rel AS solaml ON solaml.invoice_line_id = aml.id
                LEFT JOIN sale_order_line   AS sol ON sol.id = solaml.order_line_id
                LEFT JOIN sale_order        AS so ON so.id = sol.order_id
                LEFT JOIN stock_move        AS sm ON sm.sale_line_id = sol.id
                                                    AND sm.state = 'done'
                                                    AND sm.product_uom_qty = aml.quantity
                LEFT JOIN stock_valuation_layer AS svl ON svl.stock_move_id = sm.id
                LEFT JOIN stock_picking     AS sp ON sp.id = sm.picking_id
                WHERE am.move_type IN ('out_invoice', 'out_refund')
                    AND am.state = 'posted'
                    AND am.invoice_date BETWEEN '{dt_from}' AND '{dt_to}'
                    AND pt.detailed_type IN ('product', 'consu', 'service')
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
                ORDER BY am.id, am.invoice_date
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
        pre = ''
        pos = ''
        if self.partner_ids:
            wh += _add_where('am', 'partner_id', self.partner_ids)
        if self.brand_ids:
            wh += _add_where('pt', 'product_brand_id', self.brand_ids)
        if self.group_by_month:
            pre = '''
                SELECT
                    to_char(date_trunc('month', fecha)::date, 'YYYY/MM') AS mes,
                    string_agg(q.factura, ', ' ORDER BY q.factura)  AS factura,
                    cliente,
                    producto,
                    product_ref,
                    marca,
                    SUM(COALESCE(q.cantidad, 0))                AS cantidad,
                    SUM(COALESCE(q.ingreso, 0))                 AS ingreso,
                    SUM(COALESCE(q.costo, 0))                   AS costo,
                    SUM(COALESCE(q.utilidad, 0))                AS utilidad,
                    SUM(COALESCE(q.utilidad, 0)) / 
                        NULLIF(SUM(COALESCE(q.ingreso, 0)), 0)  AS p_utilidad,
                    SUM(COALESCE(q.utilidad, 0)) / 
                        NULLIF(SUM(COALESCE(q.costo, 0)), 0)    AS p_rentabilidad
                FROM (
            '''
            pos = '''
                ) AS q
                GROUP BY mes, q.cliente, q.producto, q.product_ref, q.marca
            '''

        cr = self.env.cr
        dt_from = str(self.date_from)
        dt_to = str(self.date_to)
        cr.execute(f'''
            {pre}
            SELECT
                am.invoice_date AS fecha,
                am.name         AS factura,
                rp.name         AS cliente,
                pt.name         AS producto,
                pt.default_code AS product_ref,
                pb.name         AS marca,
                aml.quantity * (CASE WHEN am.move_type = 'out_invoice' THEN 1 
                                ELSE -1 END)            AS cantidad,
                aml.amount_currency*-1                  AS ingreso,
                svl.value*-1    AS costo,
                (aml.amount_currency - svl.value)*-1    AS utilidad,
                (aml.amount_currency - svl.value) /
                NULLIF(aml.amount_currency, 0)          AS p_utilidad,
                (aml.amount_currency - svl.value) / 
                NULLIF(svl.value, 0)                    AS p_rentabilidad

            FROM account_move_line AS aml
            LEFT JOIN account_move      AS am ON am.id = aml.move_id
            LEFT JOIN res_partner       AS rp ON rp.id = am.partner_id
            LEFT JOIN product_product   AS pp ON pp.id = aml.product_id
            LEFT JOIN product_template  AS pt ON pt.id = pp.product_tmpl_id
            LEFT JOIN product_brand     AS pb ON pb.id = pt.product_brand_id
            LEFT JOIN sale_order_line_invoice_rel AS solaml ON solaml.invoice_line_id = aml.id
            LEFT JOIN sale_order_line   AS sol ON sol.id = solaml.order_line_id
            LEFT JOIN sale_order        AS so ON so.id = sol.order_id
            LEFT JOIN stock_move        AS sm ON sm.sale_line_id = sol.id 
                                                AND sm.state = 'done'
                                                AND sm.product_uom_qty = aml.quantity
            LEFT JOIN stock_valuation_layer AS svl ON svl.stock_move_id = sm.id
            LEFT JOIN stock_picking     AS sp ON sp.id = sm.picking_id
            WHERE am.move_type IN ('out_invoice', 'out_refund')
                AND am.state = 'posted'
                AND am.invoice_date BETWEEN '{dt_from}' AND '{dt_to}'
                AND pt.detailed_type IN ('product', 'consu', 'service')
                {wh}
            ORDER BY date_trunc('month', am.invoice_date)::date, rp.name, pt.name, am.name, am.invoice_date
            {pos}
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
