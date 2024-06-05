from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.types'
    _description = 'Estate Property Type'
    _order = 'name'


    name = fields.Char(string='Title', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_ids',  string='Properties')
    sequence = fields.Integer('Sequence', default=1)
    

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'The name must be unique.')
    ]