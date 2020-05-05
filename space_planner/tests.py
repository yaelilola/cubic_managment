from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from custom_user.models import CustomUser,BusinessGroup
from facilities.models import Campus, Building, Floor, Space, Cubic
from assign.models import AssignUserCubic
from CustomRequests.models import FocalPointRequest,RequestToChangeCubic
from datetime import datetime


class SpacePlannerTestCase(TransactionTestCase):
    def setUp(self):
        BusinessGroup.objects.create(id='test_group_1')
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        BusinessGroup.objects.create(id='test_group_2')
        bg2 = BusinessGroup.objects.get(id="test_group_2")
        self.user = CustomUser.objects.create_user(email='email@example.com', password='pass', employee_number='1',
                                                   percentage='part_time', business_group=bg1, focal_point=True)
        CustomUser.objects.create_user(email='space_planner@example.com', password='pass', employee_number='9',
                                       percentage='full_time', business_group=bg1, space_planner=True)
        """creating campuses"""
        Campus.objects.create(id='campus_test_1')
        campus1 = Campus.objects.get(id='campus_test_1')
        """creating buildings"""
        Building.objects.create(id='building_test_1', campus=campus1)
        building1 = Building.objects.get(id='building_test_1', campus=campus1)
        """creating floors"""
        Floor.objects.create(floor_num=1, building=building1)
        floor1 = Floor.objects.get(floor_num=1, building=building1)
        """creating spaces"""
        space1 = Space.objects.create(id='space_test_1', type='Regular', floor=floor1)
        lab1 = Space.objects.create(id='lab_1', type='Lab', floor=floor1)
        """creating cubics"""
        Cubic.objects.create(id='cubic_test_1', type='shared', business_group=bg1, area='12', space=space1)
        Cubic.objects.create(id='cubic_test_2', type='private', business_group=bg1, area='12', space=space1)
        Cubic.objects.create(id='cubic_test_3', type='shared', business_group=bg2, area='12', space=space1)
        Cubic.objects.create(id='cubic_test_4', type='private', business_group=bg1, area='12', space=space1)
        Cubic.objects.create(id='cubic_test_5', type='shared', business_group=bg1, area='12', space=space1)
        """creating full time users"""
        CustomUser.objects.create_user(email='user1@test_group_1.com', password='pass', employee_number='2',
                                       percentage='full_time', business_group=bg1)
        CustomUser.objects.create_user(email='user2@test_group_1.com', password='pass', employee_number='3',
                                       percentage='full_time', business_group=bg1)
        CustomUser.objects.create_user(email='user3@test_group_1.com', password='pass', employee_number='4',
                                       percentage='full_time', business_group=bg2)
        """creating part time users"""
        CustomUser.objects.create_user(email='user4@test_group_1.com', password='pass', employee_number='5',
                                       percentage='part_time', business_group=bg1)
        CustomUser.objects.create_user(email='user5@test_group_1.com', password='pass', employee_number='6',
                                       percentage='part_time', business_group=bg1)
        CustomUser.objects.create_user(email='user6@test_group_1.com', password='pass', employee_number='7',
                                       percentage='part_time', business_group=bg1)
        CustomUser.objects.create_user(email='user8@test_group_1.com', password='pass', employee_number='8',
                                       percentage='part_time', business_group=bg2)

    def test_simulations_GET(self):
        #function not implemented yet
        #TODO
        pass

    def test_simulations_POST(self):
        # function not implemented yet
        # TODO
        pass

    def test_get_alerts_GET(self):
        # function not implemented yet
        # TODO
        pass

    def test_get_alerts_POST(self):
        # function not implemented yet
        # TODO
        pass

    def test_assign_space_GET(self):
        # function not implemented yet
        # TODO
        pass

    def test_assign_space_POST(self):
        # function not implemented yet
        # TODO
        pass

    def test_get_building_table_GET(self):
        pass

    def test_get_floor_table_GET(self):
        pass

    def test_get_statistics_GET(self):
        pass

    def test_display_new_positions_GET(self):
        pass

    def test_display_new_positions_POST(self):
        pass

    def test_display_requests_GET(self):
        c = Client()
        c.login(email='space_planner@example.com', password='pass')
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        FocalPointRequest.objects.create(business_group=bg1, full_time_employees_amount=10,
                                         part_time_employees_amount=20)
        response = c.get(reverse('space_planner:requests'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Business Group: test_group_1')


    def test_display_request_GET(self):
        c = Client()
        c.login(email='space_planner@example.com', password='pass')
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        current_request = FocalPointRequest.objects.create(business_group=bg1, full_time_employees_amount=10,
                                         part_time_employees_amount=20)
        response = c.get(reverse('space_planner:viewrequest', kwargs={"request_id": current_request.id}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'name=\"part_time_employees_amount\" value=\"20\"')


    def test_display_request_POST(self):
        c = Client()
        c.login(email='space_planner@example.com', password='pass')
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        current_request = FocalPointRequest.objects.create(business_group=bg1, full_time_employees_amount=10,
                                                           part_time_employees_amount=20)
        response = c.post(reverse('space_planner:viewrequest', kwargs={"request_id": current_request.id}),
                          {"notes": "trying to change the request", "status": "in progress"})
        self.assertEquals(response.status_code, 302)
        response = c.get(reverse('space_planner:viewrequest', kwargs={"request_id": current_request.id}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'trying to change the request')
        self.assertContains(response, 'in progress')

    def test_assign_focal_point_GET(self):
        c = Client()
        c.login(email='space_planner@example.com', password='pass')
        response = c.get(reverse('space_planner:assignfocalpoint'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Assign Focal Point')

    def test_assign_focal_point_POST(self):
        c = Client()
        c.login(email='space_planner@example.com', password='pass')
        response = c.post(reverse('space_planner:assignfocalpoint'),
                          {"business_group": "test_group_1", "employee": "user1@test_group_1.com"})
        self.assertEquals(response.status_code, 302)
        new_focal_point = CustomUser.objects.get(email="user1@test_group_1.com")
        former_focal_point = CustomUser.objects.get(email="email@example.com")
        self.assertTrue(new_focal_point.focal_point)
        self.assertFalse(former_focal_point.focal_point)

    def test_load_employees_GET(self):
        pass

    def test_load_employees_POST(self):
        pass



