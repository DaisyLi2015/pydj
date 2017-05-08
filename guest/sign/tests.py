from django.test import TestCase
from sign.models import Event,Guest
from django.test import Client
from django.contrib.auth.models import User
from datetime import datetime

# Create your tests here.
class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=4,name="vivo 7 plus" , status =False,limit=3000,
                             address ="shanghai",start_time="2017-09-02 13:00:00")
        Guest.objects.create(id=6,event_id=4,realname="alan",phone='23214214',
                             email='alan@ylly.com',sign=False)

    # def tearDown(self):
        # Event.objects.get(id=4).delete()
        # Guest.objects.get(phone='23214214',event_id=4).delete()


    def test_event_models(self):
        result = Event.objects.get(name="vivo 7 plus")
        self.assertEqual(result.address,"shanghai")
        self.assertFalse(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='23214214')
        self.assertEqual(result.realname,"alan")
        self.assertFalse(result.sign)

class IndexPageTest(TestCase):
    "TEST INDEX LOGIN PAGE"

    def test_index_page_renders_index_template(self):
        "test index view"
        response = self.client.get("/")
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')

class LoginActionTest(TestCase):
    "test login function"

    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123456')
        self.c = Client()

    def test_login_action_username_password_null(self):
        "username is empty"
        test_data ={"username":'',"password":""}
        response =self.c.post("/login_action/",data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b"username or password error!",response.content)

    def test_login_action_username_password_error(self):
        "username is error"
        test_data = {"username": 'abs', "password": "123"}
        response = self.c.post("/login_action/", data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        "login successfully"
        test_data = {"username": 'admin', "password": "admin123456"}
        response = self.c.post("/login_action/", data=test_data)
        self.assertEqual(response.status_code, 302)

class EeventManageTest(TestCase):
    "test event manage"

    def setUp(self):
        Event.objects.create(id=5,name="huawei 7",limit=10000,status=True,
                             address="shenzhen",start_time=datetime(2017,9,12,14,0,0))
        self.c = Client()

    def test_event_manage_success(self):
        "test event :hawei 7"
        response = self.c.post("/event_manage/")
        self.assertEqual(response.status_code,200)
        self.assertIn(b"huawei 7", response.content)
        self.assertIn(b"shenzhen",response.content)

    def test_event_manage_search_success(self):
        "test event search"
        response = self.c.post("/search_name/",{"name":"huawei 7"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"huawei 7",response.content)
        self.assertIn(b"shenzhen",response.content)



class GuestManageTest(TestCase):
    "test guest manage"

    def setUp(self):
        Event.objects.create(id=4, name="vivo 7 plus", status=False, limit=3000,
                             address="shanghai", start_time=datetime(2017,9,12,14,0,0))
        Guest.objects.create(id=6, event_id=4, realname="alan", phone='23214214',
                             email='alan@ylly.com', sign=False)

        self.c = Client()

    def test_guest_manage_success(self):
        # test guest manage
        response = self.c.post("/guest_manage/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alan", response.content)
        self.assertIn(b"23214214", response.content)

    def test_guest_manage_search_success(self):
        # test guest manage search
        response = self.c.post("/guest_manage/",{"phone":"23214214"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alan", response.content)
        self.assertIn(b"23214214", response.content)

class SignIndexActionTest(TestCase):
    "test guest sign "

    def setUp(self):
        Event.objects.create(id=4, name="vivo 7 plus", status=True, limit=3000,
                             address="shanghai", start_time=datetime(2017,9,12,14,0,0))
        Event.objects.create(id=5, name="oppo 8 plus", status=True, limit=3000,
                             address="shanghai", start_time=datetime(2017, 9, 22, 14, 0, 0))
        Guest.objects.create(id=6, event_id=4, realname="alan", phone='23214214',
                             email='alan@ylly.com', sign=False)
        Guest.objects.create(id=7, event_id=5, realname="alan232", phone='12123214214',
                             email='alan23@ylly.com', sign=True)

        self.c = Client()

    def test_sign_index_action_phone_null(self):
        "phone is empty"
        response = self.c.post('/sign_index_action/4/',{"phone":""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone error.", response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        "phone or event id is error"
        response = self.c.post('/sign_index_action/5/',{"phone":"23214214"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event id or phone error.", response.content)

    def test_sign_index_action_user_sign_has(self):
        "guest has sign"
        response = self.c.post('/sign_index_action/5/',{"phone":"12123214214"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user has sign in.", response.content)

    def test_sign_index_action_sign_success(self):
        "guest sign successful"
        response = self.c.post('/sign_index_action/4/', {"phone": "23214214"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sign in success!", response.content)