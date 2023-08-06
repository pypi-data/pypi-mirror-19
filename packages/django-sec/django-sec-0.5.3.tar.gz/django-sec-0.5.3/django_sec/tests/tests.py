from __future__ import print_function

# import os
from datetime import date
import socket
import warnings
# import shutil

import six

from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth.models import User

from django_sec import models

warnings.simplefilter('error', RuntimeWarning)

socket.gethostname = lambda: 'localhost'

class Tests(TestCase):
    
    #fixtures = ['test_jobs.json']
    
    def setUp(self):
        pass
        
    def _test_example(self):
        
        # get a file from the index. it may or may not be present on our hard disk.
        # if it's not, it will be downloaded
        # the first time we try to access it, or you can call .download() explicitly
        filing = models.Index.objects\
            .filter(form='10-K', cik=1090872)\
            .order_by('-date')[0]
        
        print(filing.name)
        
        # initialize XBRL parser and populate an attribute called fields with a dict
        # of 50 common terms
        x = filing.xbrl()
        
        print(x.fields['FiscalYear'])
        
        print(x.fields)
        
        # fetch arbitrary XBRL tags representing eiter an Instant or a Duration in time
        print('Tax rate',
            x.GetFactValue('us-gaap:EffectiveIncomeTaxRateContinuingOperations', 'Duration'))
        
        if x.loadYear(1): 
            # Most 10-Ks have two or three previous years contained in them for the major values.
            # This call switches the contexts to the prior year (set it to 2 or 3 instead of 1 to
            # go back further) and reloads the fundamental concepts.
            # Any calls to GetFactValue will use that year's value from that point on.
                            
            print(x.fields['FiscalYear'])
        
            print(x.fields)
        
            print('Tax rate',
                x.GetFactValue('us-gaap:EffectiveIncomeTaxRateContinuingOperations', 'Duration'))
    
    def test_sec_import_index_attrs(self):
        
        self.assertEqual(models.Index.objects.all().count(), 0)
        self.assertEqual(models.Company.objects.all().count(), 0)
        self.assertEqual(models.Attribute.objects.all().count(), 0)
        
        # Download index file.
        out = six.StringIO()
        call_command(
            'sec_import_index',
            start_year='2016',#str(date.today().year-1),
            max_lines='20',
            quarter='1',
            traceback=True,
            dryrun=False,
            stdout=out)
        out = out.getvalue()
        print(out)
        self.assertTrue('error' not in out.lower())
        
        # The index import creates company records and index records for each company.
        self.assertTrue(models.Index.objects.all().count() > 0)
        self.assertTrue(models.Company.objects.all().count() > 0)
        self.assertEqual(models.Attribute.objects.all().count(), 0)
        self.assertEqual(models.AttributeValue.objects.all().count(), 0)
        
        # However, by default, companies aren't marked to download any attributes.
        self.assertTrue(models.Company.objects.filter(load=True).count() == 0)
        self.assertEqual(models.Attribute.objects.filter(load=True).count(), 0)
        
#         _fn = '/tmp/django_sec/company_2016_1.zip'
#         try:
#             os.remove(_fn)
#         except OSError:
#             pass
#         self.assertTrue(not os.path.isfile(_fn))
#         shutil.copy('django_sec/fixtures/company_2016_1.zip', _fn)
#         self.assertTrue(os.path.isfile(_fn))
        
        # Extract attributes from all downloaded indexes.
        out = six.StringIO()
        call_command(
            'sec_import_attrs',
            start_year=str(date.today().year-1),
            verbose=True,
            traceback=True,
            stdout=out)
        out = out.getvalue()
        print(out)
        self.assertTrue('error' not in out.lower())
        
        # No company or attribute was marked to load, so nothing should have been created.
        self.assertEqual(models.Attribute.objects.all().count(), 0)
        self.assertEqual(models.AttributeValue.objects.all().count(), 0)
        
        # Mark companies for loading attributes.
        models.Company.objects.all().update(load=True)
        # Extract attributes from all downloaded indexes.
        out = six.StringIO()
        call_command(
            'sec_import_attrs',
            start_year=str(date.today().year-1),
            verbose=True,
            traceback=True,
            stdout=out)
        out = out.getvalue()
        print(out)
        self.assertTrue('error' not in out.lower())
        
        # Many attribute and attribute value records should have been loaded.
        self.assertTrue(models.Attribute.objects.all().count() > 0)
        self.assertTrue(models.AttributeValue.objects.all().count() > 0)
    
    def _test_sec_xbrl_to_csv(self):
        call_command('sec_xbrl_to_csv')
        
    def test_sec_mark_units(self):
        unit, _ = models.Unit.objects.get_or_create(name='U_iso4217USD')
        # In Django >= 1.9, you can't set a self-referential field during creation.
        unit.save()
        self.assertTrue(unit.true_unit)
        self.assertEqual(unit.true_unit, unit)
        
        call_command('sec_mark_units')

    def test_search(self):
        #client = Client()
        user = User.objects.create(username='testuser', is_active=True, is_staff=True, is_superuser=True)
        user.set_password('12345')
        user.save()
        #self.client.force_login(user)
        self.client.login(username=user.username, password='12345')
        
        response = self.client.get('/admin/django_sec/company/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/django_sec/company/?q=abc')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/django_sec/index/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/django_sec/index/?q=abc')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/django_sec/attribute/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/django_sec/attribute/?q=abc')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/django_sec/attributevalue/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/django_sec/attributevalue/?q=abc')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/django_sec/namespace/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/django_sec/namespace/?q=abc')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/django_sec/unit/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/django_sec/unit/?q=abc')
        self.assertEqual(response.status_code, 200)
        