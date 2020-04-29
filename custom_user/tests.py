from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from .models import CustomUser, BusinessGroup
from django.urls import reverse
from facilities.models import Cubic, Campus, Building, Space, Floor
from CustomRequests.models import RequestToChangeCubic
from assign.forms import AssignPartTimeUserCubicForm
from assign.models import AssignUserCubic
from django.shortcuts import get_object_or_404
from django_webtest import WebTest


class BusinessGroupTestCase(TestCase):
    def setUp(self):
        BusinessGroup.objects.create(id='test_group_1')

    def test_group_str(self):
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        self.assertEqual(str(bg1), 'test_group_1')


class CustomUserTestCase(TestCase):
    def setUp(self):
        BusinessGroup.objects.create(id='test_group_1')
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        BusinessGroup.objects.create(id='test_group_2')
        bg2 = BusinessGroup.objects.get(id="test_group_2")
        self.user = CustomUser.objects.create_user(email='email@example.com', password='pass',employee_number='1',percentage='part_time',business_group=bg1,focal_point=True)
        """creating campuses"""
        Campus.objects.create(id='campus_test_1')
        campus1 = Campus.objects.get(id='campus_test_1')
        """creating buildings"""
        Building.objects.create(id='building_test_1',campus=campus1)
        building1 = Building.objects.get(id='building_test_1',campus=campus1)
        """creating floors"""
        Floor.objects.create(floor_num=1,building=building1)
        floor1 = Floor.objects.get(floor_num=1,building=building1)
        """creating spaces"""
        space1= Space.objects.create(id='space_test_1',type='Regular',floor=floor1)
        """creating cubics"""
        Cubic.objects.create(id='cubic_test_1', type='shared', business_group=bg1, area='12', space=space1)
        Cubic.objects.create(id='cubic_test_2', type='private', business_group=bg1, area='12', space=space1)
        Cubic.objects.create(id='cubic_test_3', type='shared', business_group=bg2, area='12', space=space1)
        Cubic.objects.create(id='cubic_test_4', type='private', business_group=bg1, area='12', space=space1)
        """creating full time users"""
        CustomUser.objects.create_user(email='user1@test_group_1.com', password='pass',employee_number='2',percentage='full_time',business_group=bg1)
        CustomUser.objects.create_user(email='user2@test_group_1.com', password='pass', employee_number='3',
                                       percentage='full_time',business_group=bg1)
        """creating part time users"""
        CustomUser.objects.create_user(email='user3@test_group_1.com', password='pass', employee_number='4',
                                       percentage='part_time', business_group=bg1)
        CustomUser.objects.create_user(email='user4@test_group_1.com', password='pass', employee_number='5',
                                       percentage='part_time', business_group=bg1)


    def test_mycubic_no_assignments_yet(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('custom_user:mycubic'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have no cubics assigned")
        user = get_object_or_404(CustomUser, email='email@example.com')
        self.assertEqual(len(AssignUserCubic.objects.filter(assigned_user=user)), 0)

    def test_assignment_part_time_post(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        c_as_focal_point = CustomUser.objects.get(email='email@example.com')
        self.assertTrue(c_as_focal_point.focal_point)
        response = c.get(reverse('focal_point:assign_part_time'))
        self.assertEqual(response.status_code, 200)
        cubic = Cubic.objects.get(id="cubic_test_1")
        user3 = CustomUser.objects.get(email='user3@test_group_1.com')
        user4 = CustomUser.objects.get(email='user4@test_group_1.com')
        c.post(reverse('focal_point:assign_part_time'), {'users': [user3,user4], 'cubics': [cubic]})
        c.logout()
        c.login(email='user3@test_group_1.com', password='pass')
        response = c.get(reverse('custom_user:mycubic'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cubic_test_1")
        c.logout()
        c.login(email='user4@test_group_1.com', password='pass')
        response = c.get(reverse('custom_user:mycubic'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cubic_test_1")

    def test_assignment_full_time_post(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        c_as_focal_point = CustomUser.objects.get(email='email@example.com')
        self.assertTrue(c_as_focal_point.focal_point)
        response = c.get(reverse('focal_point:assign_part_time'))
        self.assertEqual(response.status_code, 200)
        cubic = Cubic.objects.get(id="cubic_test_2")
        user1 = CustomUser.objects.get(email='user1@test_group_1.com')
        c.post(reverse('focal_point:assign_full_time'), {'users': [user1], 'cubics': [cubic]})
        c.logout()
        c.login(email='user1@test_group_1.com', password='pass')
        response = c.get(reverse('custom_user:mycubic'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cubic_test_2")

    def ask_to_change_cubic_post(self):
        c = Client()
        c.login(email='user1@test_group_1.com', password='pass')
        user1 = CustomUser.objects.get(email='user1@test_group_1.com')
        user_requests_amount_before = len(RequestToChangeCubic.objects.filter(user=user1))
        c.post(reverse('custom_user:createrequest'))# empty request
        user_requests_amount_after= len(RequestToChangeCubic.objects.filter(user=user1))
        self.assertEqual(user_requests_amount_before+1,user_requests_amount_after)
        cubic_test_2 = Cubic.objects.get(id='cubic_test_2')
        c.post(reverse('custom_user:createrequest'),{'cubic':cubic_test_2})# request with private cubic
        user_requests_amount_after = len(RequestToChangeCubic.objects.filter(user=user1))
        self.assertEqual(user_requests_amount_before + 2, user_requests_amount_after)
        cubic_test_1 = Cubic.objects.get(id='cubic_test_1')
        print(c.post(reverse('custom_user:createrequest'), {'cubic': cubic_test_1}))  # request with shared cubic
        user_requests_amount_after = len(RequestToChangeCubic.objects.filter(user=user1))
        self.assertEqual(user_requests_amount_before + 2, user_requests_amount_after)
        cubic_test_3 = Cubic.objects.get(id='cubic_test_3')
        print(c.post(reverse('custom_user:createrequest'), {'cubic': cubic_test_3}))  # request with another group cubic
        user_requests_amount_after = len(RequestToChangeCubic.objects.filter(user=user1))
        self.assertEqual(user_requests_amount_before + 2, user_requests_amount_after)
        cubic_test_4 = Cubic.objects.get(id='cubic_test_4')
        print(c.post(reverse('custom_user:createrequest'), {'cubic': cubic_test_4}))  # request with private cubic
        user_requests_amount_after = len(RequestToChangeCubic.objects.filter(user=user1))
        self.assertEqual(user_requests_amount_before + 3, user_requests_amount_after)

    # def test_part_time_assignment(self): """this option match django-webtest"""
    #     c_as_focal_point = CustomUser.objects.get(email='email@example.com')
    #     self.app.get('/', user=c_as_focal_point)
    #     form = self.app.get(reverse('focal_point:assign_part_time')).forms[1]
    #     form['users'] = ['user1@test_group_1.com']
    #     form['cubics'] = [Cubic.objects.get(id="cubic_test_1")]
    #     form.submit().follow()
    #     self.app.get('/', user= CustomUser.objects.get(email='user1@test_group_1.com'))
    #     response = self.app.get(reverse('custom_user:mycubic'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "cubic_test_1")






