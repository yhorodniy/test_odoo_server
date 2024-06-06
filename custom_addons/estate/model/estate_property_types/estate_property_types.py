from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.types'
    _description = 'Estate Property Type'
    _order = 'name'


    name = fields.Char(string='Title', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id',  string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Offer count', compute='_compute_offers_count')
    sequence = fields.Integer('Sequence', default=1)
    

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'The name must be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offers_count(self):
        for el in self:
            el.offer_count = len(el.offer_ids)