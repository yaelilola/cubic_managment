from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from custom_user.models import BusinessGroup
from django.urls import reverse
from facilities.models import Cubic, Campus, Building, Space, Floor
from assign.models import AssignUserCubic
from django.shortcuts import get_object_or_404
#from django_webtest import WebTest



class FacilitiesTestCase(TestCase):
    def setUp(self):
        BusinessGroup.objects.create(id='test_group_1')
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        BusinessGroup.objects.create(id='test_group_2')
        bg2 = BusinessGroup.objects.get(id="test_group_2")
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
        """creating cubics"""
        Cubic.objects.create(id='cubic_test_1', type='shared', business_group=bg1, area='12', space=space1)
        Cubic.objects.create(id='cubic_test_2', type='private', business_group=bg1, area='12', space=space1)
        Cubic.objects.create(id='cubic_test_3', type='shared', business_group=bg2, area='12', space=space1)
        Cubic.objects.create(id='cubic_test_4', type='private', business_group=bg1, area='12', space=space1)

    def test_display_campuses_GET(self):
        c = Client()
        response = c.get(reverse('facilities:campuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "campus_test_1")

    def test_display_campus_GET(self):
        c = Client()
        response = c.get(reverse('facilities:campus_buildings', kwargs={"campus_id": "campus_test_1"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "building_test_1")

    def test_display_building_GET(self):
        c = Client()
        response = c.get(reverse('facilities:building_floors', kwargs={"campus_id": "campus_test_1",
                                                                        "building_id": "building_test_1"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ID: 1")

    def test_display_floor_GET(self):
        c = Client()
        response = c.get(reverse('facilities:floor_spaces', kwargs={"campus_id": "campus_test_1",
                                                                        "building_id": "building_test_1",
                                                                     "floor_num": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "space_test_1")

    def test_display_space_GET(self):
        c = Client()
        response = c.get(reverse('facilities:space_cubics', kwargs={"campus_id": "campus_test_1",
                                                                     "building_id": "building_test_1",
                                                                     "floor_num": 1,
                                                                     "space_id": "space_test_1"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cubic_test_1")

    def test_display_cubic_GET(self):
        c = Client()
        response = c.get(reverse('facilities:cubic', kwargs={"campus_id": "campus_test_1",
                                                                     "building_id": "building_test_1",
                                                                     "floor_num": 1,
                                                                     "space_id": "space_test_1",
                                                                     "cubic_id": "cubic_test_1"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "shared")
