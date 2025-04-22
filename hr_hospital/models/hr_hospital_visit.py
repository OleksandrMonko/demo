
import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class HRHVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Visit'

    status = fields.Selection([
        ('planned', 'Planned'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], default='planned')

    planned_datetime = fields.Datetime(default=fields.Date.today(),
                                       required=True, string='Planned Date')
    actual_datetime = fields.Datetime(default=fields.Date.today(),
                                      string='Actual Visit Date')
    doctor_id = fields.Many2one('hr.hospital.doctor', string='Doctor',
                                required=True)
    patient_id = fields.Many2one('hr.hospital.patient', string='Patient',
                                 required=True)
    diagnosis_ids = fields.One2many(comodel_name='hr.hospital.diagnosis',
                                    inverse_name='visit_id',
                                    string='Diagnoses')

    @api.constrains('doctor_id', 'patient_id', 'planned_datetime')
    def _check_unique_visit(self):
        for record in self:
            if record.planned_datetime:
                existing = self.search([
                    ('id', '!=', record.id),
                    ('doctor_id', '=', record.doctor_id.id),
                    ('patient_id', '=', record.patient_id.id),
                    ('planned_datetime', '=', record.planned_datetime.date())
                ])
                if existing:
                    raise ValidationError(
                        _("Patient already has a visit with this doctor "
                          "on the same day."))

    def unlink(self):
        for record in self:
            if record.diagnosis_ids:
                raise ValidationError(
                    _("You cannot delete a visit with diagnoses."))
        return super().unlink()
