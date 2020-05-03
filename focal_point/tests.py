from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from custom_user.models import CustomUser,BusinessGroup
from facilities.models import Campus, Building, Floor, Space, Cubic
from assign.models import AssignUserCubic


class FocalPointTestCase(TransactionTestCase):
    def setUp(self):
        BusinessGroup.objects.create(id='test_group_1')
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        BusinessGroup.objects.create(id='test_group_2')
        bg2 = BusinessGroup.objects.get(id="test_group_2")
        self.user = CustomUser.objects.create_user(email='email@example.com', password='pass', employee_number='1',
                                                   percentage='part_time', business_group=bg1, focal_point=True)
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

    def test_view_assignments_GET(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:assignments'))
        self.assertContains(response, 'You made no assignments yet')
        self.assertContains(response, 'user1@test_group_1.com')
        self.assertContains(response, 'user2@test_group_1.com')
        self.assertContains(response, 'user4@test_group_1.com')
        self.assertNotContains(response, 'user3@test_group_1.com')
        c.post(reverse('focal_point:assign_full_time'),
               {'users': ['user1@test_group_1.com'], 'cubics': ['cubic_test_2']})
        response = c.get(reverse('focal_point:assignments'))
        self.assertNotContains(response, 'You made no assignments yet')
        self.assertContains(response, 'cubic_test_2')
        c = Client()
        c.login(email='user1@test_group_1.com', password='pass')
        response = c.get(reverse('focal_point:assignments'))
        self.assertEquals(response.status_code,403)

    def test_assign_part_time_GET(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        focal_point = CustomUser.objects.get(email='email@example.com')
        user1 = CustomUser.objects.get(email='user1@test_group_1.com')
        self.assertFalse(AssignUserCubic.objects.filter(assigner=focal_point).exists())
        c.post(reverse('focal_point:assign_part_time'),
               {'users': ['user3@test_group_1.com'], 'cubics': ['cubic_test_2']})
        self.assertFalse(AssignUserCubic.objects.filter(assigner=focal_point).exists())
        c.post(reverse('focal_point:assign_part_time'),
               {'users': ['user4@test_group_1.com'], 'cubics': ['cubic_test_1']})
        c.get(reverse('focal_point:assignments'))
        self.assertIsNotNone(AssignUserCubic.objects.get(assigned_user=CustomUser.objects.get(
            email='user4@test_group_1.com'), cubic=Cubic.objects.get(id="cubic_test_1")))
        c.post(reverse('focal_point:assign_part_time'),
               {'users': ['user4@test_group_1.com'], 'cubics': ['cubic_test_5']})
        c.get(reverse('focal_point:assignments'))
        self.assertTrue(AssignUserCubic.objects.filter(assigned_user=CustomUser.objects.get(
            email='user4@test_group_1.com'), cubic=Cubic.objects.get(id="cubic_test_1")).exists())
        self.assertTrue(AssignUserCubic.objects.filter(assigned_user=CustomUser.objects.get(
            email='user4@test_group_1.com'), cubic=Cubic.objects.get(id="cubic_test_5")).exists())

    def test_assign_part_time_POST(self):
        focal_point = CustomUser.objects.get(email='email@example.com')
        c = Client()
        c.login(email='email@example.com', password='pass')
        user1 = CustomUser.objects.get(email='user1@test_group_1.com')
        user4 = CustomUser.objects.get(email='user4@test_group_1.com')
        user5 = CustomUser.objects.get(email='user5@test_group_1.com')
        cubic1 = Cubic.objects.get(id="cubic_test_1")
        cubic5 = Cubic.objects.get(id="cubic_test_5")
        self.assertFalse(AssignUserCubic.objects.filter(assigner=focal_point).exists())
        c.post(reverse('focal_point:assign_part_time'),
               {'users': ['user3@test_group_1.com'], 'cubics': ['cubic_test_2']})
        self.assertFalse(AssignUserCubic.objects.filter(assigner=focal_point).exists())
        c.post(reverse('focal_point:assign_part_time'),
               {'users': ['user4@test_group_1.com'], 'cubics': ['cubic_test_1']})
        self.assertIsNotNone(AssignUserCubic.objects.get(assigned_user=user4, cubic=cubic1))
        c.post(reverse('focal_point:assign_part_time'),
               {'users': ['user4@test_group_1.com'], 'cubics': ['cubic_test_5']})
        self.assertTrue(AssignUserCubic.objects.filter(assigned_user=user4, cubic=cubic5).exists())
        c.post(reverse('focal_point:assign_part_time'),
               {'users': ['user4@test_group_1.com','user5@test_group_1.com'], 'cubics': ['cubic_test_5','cubic_test_1']})
        self.assertTrue(
            AssignUserCubic.objects.filter(assigned_user=user4, cubic=cubic5).exists())
        self.assertTrue(
            AssignUserCubic.objects.filter(assigned_user=user4, cubic=cubic1).exists())
        self.assertTrue(
            AssignUserCubic.objects.filter(assigned_user=user5, cubic=cubic5).exists())
        self.assertTrue(
            AssignUserCubic.objects.filter(assigned_user=user5, cubic=cubic1).exists())

    def test_assign_full_time_GET(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:assignments'))
        self.assertContains(response, 'You made no assignments yet')
        c.post(reverse('focal_point:assign_full_time'),
               {'users': ['user1@test_group_1.com'], 'cubics': ['cubic_test_2']})
        c.get(reverse('focal_point:assignments'))
        self.assertIsNotNone(AssignUserCubic.objects.get(assigned_user=CustomUser.objects.get(
            email='user1@test_group_1.com'), cubic=Cubic.objects.get(id="cubic_test_2")))
        c.post(reverse('focal_point:assign_full_time'),
               {'users': ['user4@test_group_1.com'], 'cubics': ['cubic_test_1']})
        self.assertFalse(AssignUserCubic.objects.filter(assigned_user=CustomUser.objects.get(
            email='user4@test_group_1.com'), cubic=Cubic.objects.get(id="cubic_test_1")).exists())
        c.post(reverse('focal_point:assign_full_time'),
               {'users': ['user2@test_group_1.com'], 'cubics': ['cubic_test_2']})
        self.assertFalse(AssignUserCubic.objects.filter(assigned_user=CustomUser.objects.get(
            email='user2@test_group_1.com'), cubic=Cubic.objects.get(id="cubic_test_2")).exists())

    def test_assign_full_time_POST(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:assignments'))
        self.assertContains(response, 'You made no assignments yet')
        c.post(reverse('focal_point:assign_full_time'),
               {'users': ['user1@test_group_1.com'], 'cubics': ['cubic_test_2']})
        self.assertIsNotNone(AssignUserCubic.objects.get(assigned_user=CustomUser.objects.get(
            email='user1@test_group_1.com'), cubic=Cubic.objects.get(id="cubic_test_2")))
        c.post(reverse('focal_point:assign_full_time'),
               {'users': ['user1@test_group_1.com'], 'cubics': ['cubic_test_3']})
        self.assertIsNotNone(AssignUserCubic.objects.get(assigned_user=CustomUser.objects.get(
            email='user1@test_group_1.com'), cubic=Cubic.objects.get(id="cubic_test_2")))
        self.assertFalse(AssignUserCubic.objects.filter(assigned_user=CustomUser.objects.get(
            email='user1@test_group_1.com'), cubic=Cubic.objects.get(id="cubic_test_3")).exists())

    """also tests test_edit_for_user, which does not have a url"""
    def test_view_assignments_for_user_GET(self):
        focal_point = CustomUser.objects.get(email='email@example.com')
        c = Client()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:assignments'))
        self.assertContains(response, 'You made no assignments yet')
        """full time"""
        user1 = CustomUser.objects.get(email='user1@test_group_1.com')
        user2 = CustomUser.objects.get(email='user2@test_group_1.com')
        cubic_test_2 = Cubic.objects.get(id='cubic_test_2')
        AssignUserCubic.objects.create(assigner=focal_point,assigned_user=user1,cubic=cubic_test_2)
        response = c.get(reverse('focal_point:viewuserassignments', kwargs={'user_id':user1.id}))
        self.assertContains(response,'<option value="cubic_test_2" selected>cubic_test_2</option>')
        response = c.get(reverse('focal_point:viewuserassignments', kwargs={'user_id': user2.id}))
        self.assertNotContains(response, '<option value="cubic_test_2">cubic_test_2</option>')
        """part time"""
        user3 = CustomUser.objects.get(email='user3@test_group_1.com')
        user4 = CustomUser.objects.get(email='user4@test_group_1.com')
        user5 = CustomUser.objects.get(email='user5@test_group_1.com')
        user6 = CustomUser.objects.get(email='user6@test_group_1.com')
        cubic_test_1 = Cubic.objects.get(id='cubic_test_1')
        cubic_test_5 = Cubic.objects.get(id='cubic_test_5')
        response = c.get(reverse('focal_point:viewuserassignments', kwargs={'user_id': user3.id}))
        self.assertEquals(response.status_code,403)
        AssignUserCubic.objects.create(assigner=focal_point, assigned_user=user4, cubic=cubic_test_1)
        AssignUserCubic.objects.create(assigner=focal_point, assigned_user=user4, cubic=cubic_test_5)
        AssignUserCubic.objects.create(assigner=focal_point, assigned_user=user5, cubic=cubic_test_1)
        AssignUserCubic.objects.create(assigner=focal_point, assigned_user=user5, cubic=cubic_test_5)
        response = c.get(reverse('focal_point:viewuserassignments', kwargs={'user_id': user4.id}))
        self.assertContains(response, '<option value="cubic_test_1" selected>cubic_test_1</option>')
        self.assertContains(response, '<option value="cubic_test_5" selected>cubic_test_5</option>')
        response = c.get(reverse('focal_point:viewuserassignments', kwargs={'user_id': user5.id}))
        self.assertContains(response, '<option value="cubic_test_1" selected>cubic_test_1</option>')
        self.assertContains(response, '<option value="cubic_test_5" selected>cubic_test_5</option>')
        response = c.get(reverse('focal_point:viewuserassignments', kwargs={'user_id': user6.id}))
        self.assertNotContains(response, '<option value="cubic_test_1">cubic_test_1</option>')
        self.assertNotContains(response, '<option value="cubic_test_5">cubic_test_5</option>')

    """also tests test_edit_for_user, which does not have a url"""
    def test_view_assignments_for_user_POST(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:assignments'))
        self.assertContains(response, 'You made no assignments yet')
        """full time"""
        user1 = CustomUser.objects.get(email='user1@test_group_1.com')
        user2 = CustomUser.objects.get(email='user2@test_group_1.com')
        cubic_test_2 = Cubic.objects.get(id='cubic_test_2')
        c.post(reverse('focal_point:viewuserassignments', kwargs={'user_id':user1.id}),
               {'users': ['user1@test_group_1.com'], 'cubics': ['cubic_test_2']})
        self.assertTrue(AssignUserCubic.objects.filter(assigned_user=user1,cubic=cubic_test_2).exists())
        self.assertFalse(AssignUserCubic.objects.filter(assigned_user=user2, cubic=cubic_test_2).exists())
        c.post(reverse('focal_point:viewuserassignments', kwargs={'user_id': user1.id}),
               {'users': ['user1@test_group_1.com'], 'cubics': ['cubic_test_2','cubic_test_4']})
        self.assertEquals(len(AssignUserCubic.objects.filter(assigned_user=user1)), 1)
        """part time"""
        user3 = CustomUser.objects.get(email='user3@test_group_1.com')
        user4 = CustomUser.objects.get(email='user4@test_group_1.com')
        user5 = CustomUser.objects.get(email='user5@test_group_1.com')
        user6 = CustomUser.objects.get(email='user6@test_group_1.com')
        response = c.post(reverse('focal_point:viewuserassignments', kwargs={'user_id': user3.id}))
        self.assertEquals(response.status_code, 403)
        c.post(reverse('focal_point:viewuserassignments', kwargs={'user_id': user4.id}),
               {'users': ['user4@test_group_1.com'], 'cubics': ['cubic_test_1', 'cubic_test_5']})
        c.post(reverse('focal_point:viewuserassignments', kwargs={'user_id': user5.id}),
               {'users': ['user5@test_group_1.com'], 'cubics': ['cubic_test_1', 'cubic_test_5']})
        cubic_test_1 = Cubic.objects.get(id='cubic_test_1')
        cubic_test_5 = Cubic.objects.get(id='cubic_test_5')
        self.assertTrue(AssignUserCubic.objects.filter(assigned_user=user4,cubic=cubic_test_1).exists())
        self.assertTrue(AssignUserCubic.objects.filter(assigned_user=user4, cubic=cubic_test_5).exists())
        self.assertTrue(AssignUserCubic.objects.filter(assigned_user=user5, cubic=cubic_test_1).exists())
        self.assertTrue(AssignUserCubic.objects.filter(assigned_user=user5, cubic=cubic_test_5).exists())

    def test_delete_all_user_assignments_POST(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:assignments'))
        self.assertContains(response, 'You made no assignments yet')
        """full time"""
        user1 = CustomUser.objects.get(email='user1@test_group_1.com')
        user2 = CustomUser.objects.get(email='user2@test_group_1.com')
        c.post(reverse('focal_point:assign_full_time'),
               {'users': ['user1@test_group_1.com'], 'cubics': ['cubic_test_2']})
        response = c.get(reverse('focal_point:viewuserassignments', kwargs={'user_id': user1.id}))
        self.assertContains(response, '<option value="cubic_test_2" selected>cubic_test_2</option>')
        c.post(reverse('focal_point:delete_all_user_assignments',kwargs={'user_id': user1.id}))
        self.assertFalse(AssignUserCubic.objects.filter(assigned_user=user1).exists())

    def test_create_request_GET(self):
        pass

    def test_create_request_POST(self):
        pass

    def test_display_requests_GET(self):
        pass

    def test_display_request_GET(self):
        pass

    def test_display_request_POST(self):
        pass

    def test_display_my_requests_GET(self):
        pass

    def test_display_my_request_GET(self):
        pass

    def test_display_my_request_POST(self):
        pass

    def test_display_new_positions_GET(self):
        pass

    def test_delete_request_POST(self):
        pass
