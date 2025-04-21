from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit', string='Visit', required=True)
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease', string='Disease', required=True)
    description = fields.Text(string='Treatment Description')
    is_approved = fields.Boolean()

    diagnosis_date = fields.Datetime(
        compute='_compute_data',
        store=True)

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        compute='_compute_data',
        domain=[('is_intern)','=',False)],
        store=True)

    @api.depends('visit_id')
    def _compute_data(self):
        for record in self:
            if record.visit_id:
                record.doctor_id = record.visit_id.doctor_id.id
                record.diagnosis_date = record.visit_id.planned_datetime

    @api.constrains('approved')
    def _check_mentor_approval(self):
        for record in self:
            doctor = record.visit_id.doctor_id
            if (doctor.is_intern and record.is_approved
                    and not doctor.mentor_id):
                raise ValidationError(
                    _("Intern's diagnosis must be approved by a mentor."))
