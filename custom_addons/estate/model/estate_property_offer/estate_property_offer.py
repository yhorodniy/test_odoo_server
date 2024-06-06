from datetime import timedelta
from odoo import api, exceptions, fields, models
from odoo.tools.float_utils import float_compare


class EstatePropertyTag(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'


    price = fields.Float(string='Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_state = fields.Selection(related='property_id.state')
    property_type_id = fields.Many2one(related='property_id.property_type_id')
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'Price should be only pisitive')
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for el in self:
            el.date_deadline = fields.Date.today() + timedelta(days=el.validity)

    @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for el in self:
            if el.date_deadline:
                deadline_date = fields.Date.from_string(el.date_deadline)
                delta = deadline_date - fields.Date.today()
                el.validity = delta.days

    def action_accept(self):
        self.ensure_one()
        property = self.property_id
        if property.state == 'offer_accepted':
            raise exceptions.UserError('Неможливо прийняти пропозицію, зі статусом "Прийнято пропозицію"')

        max_sell_price = property.expected_price
        sell_prise = self.price
        if (float_compare(sell_prise, max_sell_price * 0.9, precision_digits=2) == -1):
            raise exceptions.UserError('Неможливо прийняти пропозицію, оскільки ціна нижча за очікувану')
        property.state = 'offer_accepted'
        property.buyer_id = self.partner_id
        property.selling_price = sell_prise
        self.status = 'accepted'

    def action_refuse(self):
        self.ensure_one()
        property = self.property_id
        if property.state == 'offer_received':
            raise exceptions.UserError('Неможливо відхилити пропозицію, зі статусом "Скасована пропозиція"')
        self.status = 'refused'

    @api.model
    def create(self, vals):
        property_record = self.env['estate.property'].browse(vals.get('property_id'))

        if property_record.state == 'new':
            property_record.write({'state': 'offer_received'})
        else:
            valid_offer_price = max(property_record.offer_ids.mapped('price'), default=0)
            if vals.get('price') <= valid_offer_price:
                raise exceptions.ValidationError(f'The offer price must be more than {valid_offer_price}')

        return super().create(vals)