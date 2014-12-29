from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

PROCUREMENT_PRIORITIES = [('0', 'Not urgent'), ('1', 'Normal'), ('2', 'Urgent'), ('3', 'Very Urgent')]

class procurement_wizard(osv.Model):
    _name = 'procurement.wizard'

    _columns = {
        'name': fields.text('Description', required=True),

        'origin': fields.char('Source Document',
            help="Reference of the document that created this Procurement.\n"
            "This is automatically completed by Odoo."),
        'company_id': fields.many2one('res.company', 'Company', required=True),

        # These two fields are used for shceduling
        'priority': fields.selection(PROCUREMENT_PRIORITIES, 'Priority', required=True, select=True, track_visibility='onchange'),
        'date_planned': fields.datetime('Scheduled Date', required=True, select=True, track_visibility='onchange'),

        'group_id': fields.many2one('procurement.group', 'Procurement Group'),
        'rule_id': fields.many2one('procurement.rule', 'Rule', track_visibility='onchange', help="Chosen rule for the procurement resolution. Usually chosen by the system but can be manually set by the procurement manager to force an unusual behavior."),

        'product_id': fields.many2one('product.product', 'Product', required=True),
        'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), required=True,),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),

        'product_uos_qty': fields.float('UoS Quantity'),
        'product_uos': fields.many2one('product.uom', 'Product UoS'),

    }

    def action_create_procurements(self, cr, uid, ids, context=None):
        vals={}
        for record in self.browse(cr, uid, ids, context=None):
            vals={
                'name': record.name,
                'origin': record.origin,
                'company_id': record.company_id,

            }
