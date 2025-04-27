import logging

from odoo import models, fields, api
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class HRHDoctor(models.Model):
    _inherit = 'hr.hospital.person.mixin'
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    specialty_id = fields.Many2one(
        comodel_name='hr.hospital.specialty', string='Specialty')
    is_intern = fields.Boolean(string='Intern')
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor', string='Mentor',
        domain=[('is_intern', '=', False)])

    interns_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='mentor_id')

    patients_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='personal_doctor_id')

    color = fields.Char(
        compute="_compute_color",
        store=True)

    @api.depends('specialty_id')
    def _compute_color(self):
        for record in self:
            if record.specialty_id.id == 'hr_hospital_specialty_1':
                record.color = '#FF0000'
            elif record.specialty_id.id == 'hr_hospital_specialty_2':
                record.color = '#00FF00'
            elif record.specialty_id.id == 'hr_hospital_specialty_3':
                record.color = '#FFD700'
            else:
                record.color = '#FFFFFF'

    @api.constrains('mentor_id')
    def _check_mentor_not_intern(self):
        for record in self:
            if record.mentor_id and record.mentor_id.is_intern:
                raise models.ValidationError(
                    _("An intern cannot be a mentor."))

    def create_visit(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Visit',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_doctor_id': self.id,
            },
        }
