from django.test import TestCase
from .models import UserEvent, User, UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.

class URLTests(TestCase):
    def setUp(self):
        event = UserEvent(id=10, name="test", description="testing", category="Food", date="2022-10-30", start_time="09:00:00", end_time="10:00:00")
        event.save()
        self.event = event
        self.event_id = 10

        user_a = User(username="unittest", email="unittest@gmail.com")
        user_a_user = 'unittest'
        user_a_pw = 'unittesting'
        self.user_a_pw = user_a_pw
        self.user_a_user = user_a_user
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a
        user_a_profile = UserProfile(user=user_a, age=20, contactNo=98271828, address="Bukit Batok Street 30 Blk 201", neighbourhood="Jurong East")
        user_a_profile.save()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_eventpage(self):
        response = self.client.get('/view_event/'+str(self.event_id), follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_profilepage(self):
        data = {"username": self.user_a_user, "password": self.user_a_pw}
        self.client.post("/login/", data, follow=True)
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
    
    def test_profileEventspage(self):
        data = {"username": self.user_a_user, "password": self.user_a_pw}
        self.client.post("/login/", data, follow=True)
        response = self.client.get('/profileEvents/')
        self.assertEqual(response.status_code, 200)
    
    def test_participationfunction(self):
        data = {"username": self.user_a_user, "password": self.user_a_pw}
        self.client.post("/login/", data, follow=True)
        self.client.get('/view_event/'+str(self.event_id), follow=True)
        response = self.client.post("/participate/"+str(self.event_id), follow=True)
        self.assertEqual(response.status_code, 200)
    



class UserTests(TestCase):

    def setUp(self):
        user_a = User(username="unittest", email="unittest@gmail.com")
        user_a_user = 'unittest'
        user_a_pw = 'unittesting'
        self.user_a_pw = user_a_pw
        self.user_a_user = user_a_user
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a
        user_a_profile = UserProfile(user=user_a, age=20, contactNo=98271828, address="Bukit Batok Street 30 Blk 201", neighbourhood="Jurong East")
        user_a_profile.save()
    
    def test_user_exists(self):
        user_count = UserProfile.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_user_password(self):
        self.assertTrue(self.user_a.check_password(self.user_a_pw))
    
    def test_login_url(self):
        data = {"username": self.user_a_user, "password": self.user_a_pw}
        response = self.client.post("/login/", data, follow=True)
        self.assertEqual(response.status_code, 200)
