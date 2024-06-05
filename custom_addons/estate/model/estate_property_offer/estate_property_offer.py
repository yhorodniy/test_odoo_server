from datetime import datetime, timedelta
from odoo import api, exceptions, fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"


    price = fields.Float(
        string="Price",
        constraint=[
            'check_price_positive',
            'CHECK(price > 0)',
            'Expected price should be strictly positive'
        ]
    )
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'Price should be only pisitive')
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                delta = record.date_deadline - fields.Date.today()
                record.validity = delta.days

    def action_accept(self):
        self.ensure_one()
        property = self.property_id
        print('*'*50)
        print(property.state)
        if property.state == "offer_received":
            raise exceptions.UserError('Неможливо прийняти пропозицію, зі статусом "Отримано пропозицію"')
        property.state = "offer_accepted"
        property.buyer_id = self.partner_id
        property.selling_price = self.price
        self.status = "accepted"

    def action_refuse(self):
        self.ensure_one()
        property = self.property_id
        if property.state == "offer_received":
            raise exceptions.UserError('Неможливо відхилити пропозицію, зі статусом "Отримано пропозицію"')
        self.status = "refused"
