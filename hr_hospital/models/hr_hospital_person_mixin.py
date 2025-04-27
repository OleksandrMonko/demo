
from odoo import models, fields


class HRHPerson(models.AbstractModel):
    _name = 'hr.hospital.person.mixin'
    _description = 'Abstract Person'

    name = fields.Char(compute='_compute_name',)
    description = fields.Text()
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    phone = fields.Char()
    user_id = fields.Many2one(
        comodel_name='res.users',
        ondelete='set null',
        default=lambda self: self.env.user)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], )
    image_1920 = fields.Image(string="Photo")

    def _compute_name(self):
        for record in self:
            record.name = f'{record.first_name} {record.last_name}'
