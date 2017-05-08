import hashlib
import unittest
from datetime import time

import requests


class AddEventTestSec(unittest.TestCase):

    def setUp(self):
        self.base_url="http://127.0.0.1:8000/api/sec_add_event"
        # app_key
        self.api_key = "&Guest-Bugmaster"
        # current time
        now_time =time()
        self.client_time = str(now_time).split('.')[0]
        # sign
        md5 = hashlib.md5()
        sign_str = self.client_time+self.api_key
        sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()

    def test_add_event_sign_null(self):
        '''sign para is empty'''
        payload = {'eid':1,'':'','limit':'','address':'','start_time':'',
                   'time':'','sign':''}
        r = requests.post(self.base_url,data=payload)
        result = r.json()
        self.assertEqual(result['status'],10011)
        self.assertEqual(result['message'],'user sign null')

    def test_add_event_time_out(self):
        '''timeout'''
        now_time = str(int(self.client_time)-61)
        payload = {'eid':1,'':'','limit':'','address':'','start_time':'',
                   'time':'now_time','sign':'abc'}
        r = requests.post(self.base_url,data=payload)
        result = r.json()
        self.assertEqual(result['status'],10012)
        self.assertEqual(result['message'],'user sign timeout')

    def test_add_event_sign_error(self):
        '''sign error'''
        payload = {'eid':1,'':'','limit':'','address':'','start_time':'',
                   'time':'self.client_time','sign':'abc'}
        r = requests.post(self.base_url,data=payload)
        result = r.json()
        self.assertEqual(result['status'],10013)
        self.assertEqual(result['message'],'user sign error')

    def test_add_event_success(self):
        '''add event successfully'''
        payload = {'eid': 11, 'name': '234phone event', 'limit': '3000',
                   'address': 'beijing', 'start_time': '2017-10-23 12:00:00',
                   'time': 'self.client_time', 'sign': self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'add event success')