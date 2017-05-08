import requests
import unittest

class GetEventListTest(unittest.TestCase):

    # search event interface

    def setUp(self):
        self.url ="http://127.0.0.1:8000/api/get_event_list"

    def test_get_event_null(self):
        "event id is null"
        r =requests.get(self.url,params={'eid':''})
        result = r.json()
        print(result)
        self.assertEqual(result['status'],10021)
        self.assertEqual(result['message'], "parameter error")

    def test_get_event_success(self):
        "get event successfully"
        r = requests.get(self.url,params={'eid':'1'})
        result =r.json()
        print(result)
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")
        self.assertEqual(result['data']['name'],'iphone 8 发布会')
        self.assertEqual(result['data']['address'], '北京鸟巢')
        self.assertEqual(result['data']['start_time'], '2017-10-07T06:01:50')

if __name__=='__main__':
    unittest.main()