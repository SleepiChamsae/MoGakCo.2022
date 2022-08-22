
from django.test import TestCase

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "MoGakCo.MoGakCo.settings")

import django
django.setup()

from datetime import datetime

from MoGakCo.first.views import waiting
from MoGakCo.first.models import *


class ViewsTest(TestCase):
    def testGetTime(self):
        t = waiting.getNextTime()
        self.assertTrue(datetime.now() < t)

    def testGetNewTime(self):
        t = waiting.getNewTime()
        try:
            Time.next_time.get(t, )
        except Exception as e:
            print(e)
            self.assertTrue(False)
        self.assertTrue(datetime.now() < t)
