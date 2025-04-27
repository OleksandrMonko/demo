from datetime import datetime
from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError


class TestHospitalVisit(TransactionCase):

    def setUp(self):
        super().setUp()
        # Створення тестових даних: лікар, пацієнт, хвороба
        self.patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Donald',
            'last_name': 'Douglas',
        })
        self.doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'Dr.',
            'last_name': 'House',
        })
        self.disease = self.env['hr.hospital.disease'].create({
            'name': 'Appendicitis',
        })

    def test_write_with_completed_status(self):
        # Створення візиту
        visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_datetime': datetime(2025, 4, 22, 12, 30),
            'status': 'done',
        })
        # Спроба змінити час або лікаря для візиту зі статусом "done"
        with self.assertRaises(ValidationError):
            visit.write({'planned_datetime': datetime(2025, 4, 23, 11, 0)})

    def test_check_patient_doctor_schedule(self):
        # Створення першого візиту
        self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_datetime': datetime(2025, 4, 23, 10, 0),
        })
        # Створення другого візиту для
        # того ж пацієнта і лікаря на той самий день
        with self.assertRaises(ValidationError):
            self.env['hr.hospital.visit'].create({
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'planned_datetime': datetime(2025, 4, 23, 11, 0),
            })

    def test_unlink_with_diagnosis(self):
        # Створення візиту
        visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_datetime': datetime(2025, 4, 23, 11, 0),
        })
        # Створення діагнозу для візиту
        self.env['hr.hospital.diagnosis'].create({
            'visit_id': visit.id,
            'disease_id': self.disease.id,
        })
        # Спроба видалити візит, який має діагноз
        with self.assertRaises(ValidationError):
            visit.unlink()

    def test_write_without_completed_status(self):
        # Створення візиту
        visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_datetime':
                datetime(2025, 4, 23, 11, 0),
            'status': 'planned',
        })
        # Спроба змінити час для візиту, який ще не завершений
        visit.write({'planned_datetime': datetime(2025, 4, 23, 11, 0)})
        self.assertEqual(visit.planned_datetime,
                         datetime(2025, 4, 23, 11, 0),
                         "Час візиту не був оновлений")
