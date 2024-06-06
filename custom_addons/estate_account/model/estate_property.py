from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'


    def set_is_sold(self):
        buyer = self.buyer_id.id
        percent_of_selling_price = self.selling_price * 0.06
        admin_fees = 100.00

        values = {
            'partner_id': buyer,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': '6% of Selling Price',
                    'quantity': 1,
                    'price_unit': percent_of_selling_price,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': admin_fees, 
                })
            ]
        }


        self.env['account.move'].create(values)