{
    'name': 'HR Hospital',
    'summary': '',
    'author': 'Oleksandr Monko',
    'website': 'https://odoo.school/',
    'category': 'Customizations',
    'license': 'OPL-1',
    'version': '17.0.2.1.0',

    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': [],
    },

    'data': [
        'security/ir.model.access.csv',
        'data/hr.hospital.disease.data.csv',
        'views/hr_hospital_menu.xml',
        'views/hr_hospital_views.xml',
    ],
    'demo': [
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr_hospital_patient_demo.xml',
    ],

    'installable': True,
    'auto_install': False,
    'images': [
        'static/description/icon.png',
    ],
}
