from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from core.models import Userprofile
from employer.company.models import Company
from employer.job.models import Category, Job

USER_MODEL = get_user_model()


class JobDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = USER_MODEL.objects.create(
            username='Elsa',
            email='elsa@gmail.com',
            password='8096546qWe',
        )
        self.userprofile_employer = Userprofile.objects.create(
            user=self.user, is_employer=True
        )
        self.company = Company.objects.create(
            name='Google',
            slug='google',
            employer=self.userprofile_employer,
            field_of_activity='Internet',
            short_description='We are the largest tech company in the world',
            location='Menlo Park, CA',
            created_at='1998',
            amount_of_workers='10 - 99',
            phone='+38076321238',
            website='https://www.google.com/',
            email='support.google@gmail.com',
            company_detail='Join Us now!',
        )
        self.category = Category.objects.create(
            title='Technology',
            slug='technology',
            ordering='1',
        )
        self.job = Job.objects.create(
            title='Senior back-end developer',
            slug='senior-back-end-developer',
            short_description='Senior back-end developer',
            category=self.category,
            company=self.company,
            application_url='https://www.facebook.com/',
            location='Minsk, Belarus',
            type_of_employment='Full time',
            salary='80.000$ / year',
            working_hours='45 / week',
            experience='7 years',
            academic_degree='Bachelor',
            job_detail='Senior back-end developer',
        )

    def test_get_detail_vew(self):
        """Tests that a GET request works properly"""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('job_detail', kwargs={'company_slug': self.job.company.slug, 'slug': self.job.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job/job_detail.html')
