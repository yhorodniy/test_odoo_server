from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'


    name = fields.Char(string='Title', required=True)
    color = fields.Integer()

    _sql_constraints = [
        (
            "unique_property_type_name",
            "UNIQUE(name)",
            "The name must be unique.",
        )
    ]