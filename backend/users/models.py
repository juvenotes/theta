from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import IndexedTimeStampedModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, IndexedTimeStampedModel):

    STUDENT = 'ST'
    PROFESSIONAL = 'PR'

    ROLE_CHOICES = [ # noqa: RUF012
        (STUDENT, 'Student'),
        (PROFESSIONAL, 'Professional'),
    ]

    MEDICAL_STUDENT = 'MS'
    NURSING_STUDENT = 'NS'
    PHARMACY_STUDENT = 'PS'
    DENTAL_SURGERY_STUDENT = 'DS'

    DOCTOR = 'DR'
    NURSE = 'NR'
    PHARMACIST = 'PH'
    DENTIST = 'DT'

    STUDENT_CHOICES = [  # noqa: RUF012
        (MEDICAL_STUDENT, 'Medical Student'),
        (NURSING_STUDENT, 'Nursing Student'),
        (PHARMACY_STUDENT, 'Pharmacy Student'),
        (DENTAL_SURGERY_STUDENT, 'Dental Surgery Student'),
    ]

    PROFESSIONAL_CHOICES = [  # noqa: RUF012
        (DOCTOR, 'Doctor'),
        (NURSE, 'Nurse'),
        (PHARMACIST, 'Pharmacist'),
        (DENTIST, 'Dentist'),
    ]

    INSTITUTION_CHOICES = [  # noqa: RUF012
        ('UON', 'University of Nairobi'),
        ('KU', 'Kenyatta University'),
        ('AKU', 'Aga Khan University'),
        ('MKU', 'Mount Kenya University'),
        ('JKUAT', 'JKUAT'),
        ('EG', 'Egerton'),
        ('MMUST', 'MMUST'),
        ('MSU', 'Maseno University'),
    ]

    CURRENT_YEAR = datetime.now().year
    GRADUATION_YEAR_CHOICES = [(r,r) for r in range(2000, CURRENT_YEAR+1)] # noqa: RUF012

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    is_staff = models.BooleanField(
        default=False, help_text=_("Designates whether the user can log into this admin site.")
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, blank=True)
    student_profession = models.CharField(max_length=2, choices=STUDENT_CHOICES+PROFESSIONAL_CHOICES, blank=False, default='MS')
    institution = models.CharField(max_length=5, choices=INSTITUTION_CHOICES, blank=False, default='UON')
    graduation_year = models.IntegerField(choices=GRADUATION_YEAR_CHOICES, blank=False, default=2024)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # noqa: RUF012

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
