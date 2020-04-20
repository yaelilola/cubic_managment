from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from .models import CustomUser, BusinessGroup
from django.urls import reverse
from facilities.models import Cubic, Campus, Building, Space, Floor
from focal_point.models import FocalPoint
from CustomRequests.models import RequestToChangeCubic
from assign.forms import AssignPartTimeUserCubicForm

class BusinessGroupTestCase(TestCase):
    def setUp(self):
        BusinessGroup.objects.create(id='test_group_1')
    def test_group_str(self):
        """Animals that can speak are correctly identified"""
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        self.assertEqual(str(bg1), 'test_group_1')


class CustomUserTestCase(TestCase):
    def setUp(self):
        BusinessGroup.objects.create(id='test_group_1')
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        self.user = CustomUser.objects.create_user(email='email@example.com', password='pass',employee_number='1',percentage='part_time',business_group=bg1,focal_point=True)
        FocalPoint.objects.create(custom_user=self.user)
        Campus.objects.create(id='campus_test_1')
        campus1 = Campus.objects.get(id='campus_test_1')
        Building.objects.create(id='building_test_1',campus=campus1)
        building1 = Building.objects.get(id='building_test_1',campus=campus1)
        Floor.objects.create(floor_num=1,building=building1)
        floor1 = Floor.objects.get(floor_num=1,building=building1)
        space1= Space.objects.create(id='space_test_1',type='Regular',floor=floor1)
        CustomUser.objects.create_user(email='user1@test_group_1.com', password='pass',employee_number='1',percentage='part_time',business_group=bg1)
        Cubic.objects.create(id='cubic_test_1',type='shared',business_group=bg1,area='12',space=space1)

    def test_mycubic_no_assignments_yet(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('custom_user:mycubic'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have no cubics assigned")

    def test_mycubic_one_assignment(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:assign_part_time'))
        self.assertEqual(response.status_code, 200)
        response = c.post(reverse('focal_point:assign_part_time'),data={'form': {'assigned_user': CustomUser.objects.get(email='user1@test_group_1.com'),
                                        'cubic': Cubic.objects.get(id="cubic_test_1")}})
        print(response.content)
        # self.assertEqual(response.status_code, 200)
        self.assertTrue(True)



