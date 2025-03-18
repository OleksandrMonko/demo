import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HRHVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Visit'

    name = fields.Char(srting='Visit')

    description = fields.Text()
    date = fields.Datetime()

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient', string='papient', required=True)

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor', string='doctor', required=True)

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='disease', required=True)
