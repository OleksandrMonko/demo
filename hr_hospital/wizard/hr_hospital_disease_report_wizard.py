from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Wizard for generating disease report'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
        required=False
    )

    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
        required=False
    )

    date_from = fields.Date(
        string='From Date',
        required=True
    )
    date_to = fields.Date(
        string='To Date',
        required=True
    )

    @api.constrains('date_from', 'date_to')
    def _check_date_range(self):
        for record in self:
            if record.date_from > record.date_to:
                raise ValidationError(
                    _("The 'From Date' should be before /"
                      " or equal to the 'To Date'."))

    # def _get_report_base_filename(self):
    #    self.ensure_one()
    #    return 'Report - %s' % (self.date_from)

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids')
        res['doctor_ids'] = [(6, 0, active_ids)]
        return res

    def get_disease_report(self):
        domain = []

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        domain.append(('diagnosis_date', '>=', self.date_from))

        domain.append(('diagnosis_date', '<=', self.date_to))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Disease report',
            'res_model': 'hr.hospital.diagnosis',
            'view_mode': 'list',
            'view_type': 'form',
            'domain': domain,
            'target': 'inline',
            'context': {'group_by': 'disease_id'},
        }
