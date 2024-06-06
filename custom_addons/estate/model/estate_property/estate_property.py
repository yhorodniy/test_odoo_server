from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    __description = 'Estate property description'
    _order = 'id desc'

    def _defaultData(self):
        return datetime.today() + relativedelta(month=3)

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Availability Date', copy=False, default=_defaultData)
    expected_price = fields.Float(
        string='Expected Price',
        required=True,
    )
    selling_price = fields.Float( tring='Selling Price', eadOnly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    total_area = fields.Float(compute='_compute_total', string='Total area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        required=True,
        copy=False,
        default='new'
    )
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)

    property_type_ids = fields.Many2one('estate.property.types', string='Property Type')
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(
        compute="_compute_best_price",
        string="Best price",
    )

    _sql_constraints = [
        ("check_expected_price_positive", "CHECK(expected_price > 0)", "Expected price should be strictly positive"),
        ("check_best_price_positive", "CHECK(best_price > 0)", "Selling price should be strictly positive")
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = (record.living_area + record.garden_area) / 1000

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = ""

    def set_is_cancel(self):
        self.ensure_one()
        if self.state == "sold":
            raise exceptions.UserError("Неможливо скасувати продану власність")
        else:
            self.state = "canceled"

    def set_is_sold(self):
        self.ensure_one()
        if self.state == "canceled":
            raise exceptions.UserError("Неможливо продати скасовану власність")
        else:
            self.state = "sold"