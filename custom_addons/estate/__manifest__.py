{
    'name': "estate",
    'depends': [
        'base_setup',
        'sales_team',
        'mail',
        'calendar',
        'resource',
        'utm',
        'web_tour',
        'contacts',
        'digest',
        'phone_validation',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menu.xml',
        'views/estate_search.xml',
        'views/estate_property_views.xml',
        'views/estate_property_types_views.xml',
    ],
    'application': True,
}