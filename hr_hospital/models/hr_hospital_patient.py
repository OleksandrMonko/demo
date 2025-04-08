import logging

from datetime import date
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HRHPatient(models.Model):
    _inherit = 'hr.hospital.person.mixin'
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Personal doctor')

    birthday = fields.Date()
    age = fields.Integer(compute='_compute_age', store=True)
    passport_id = fields.Char(string='Passport')
    contact_person = fields.Char()

    @api.depends('birthday')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if not record.birthday:
                record.age = 0
                continue

            age = today.year - record.birthday.year
            if today.month < record.birthday.month:
                age -= 1
            elif today.month == record.birthday.month:
                if today.day < record.birthday.day:
                    age -= 1

            record.age = age
