import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HRHPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    name = fields.Char()
    description = fields.Text()
    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor',
                                string='Doctor')
