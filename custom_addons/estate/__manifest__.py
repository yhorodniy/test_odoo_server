{
    'name': "estate",
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_search.xml',
        'views/estate_property_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_user_view.xml',
        'views/estate_menu.xml',
        'views/estate_property_kanban.xml',
    ],
    'application': True,
}