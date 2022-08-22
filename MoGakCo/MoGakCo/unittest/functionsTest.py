from unittest import *

from functions import *


class DateTimeTest(TestCase):
    def setUp(self):
        self.date_time = date_time()

    def testKorTime(self):
        self.assertEqual(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.date_time.getKorTime().strftime('%Y-%m-%d %H:%M:%S'))

    def testRandomTime(self):
        self.assertTrue(getNextRandomDate() > datetime.utcnow())
