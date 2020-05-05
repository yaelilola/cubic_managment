from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from custom_user.models import CustomUser,BusinessGroup
from facilities.models import Campus, Building, Floor, Space, Cubic
from assign.models import AssignUserCubic
from CustomRequests.models import FocalPointRequest,RequestToChangeCubic
from recruit.models import NewPosition
from datetime import datetime

class FocalPointTestCase(TransactionTestCase):
    def setUp(self):
        BusinessGroup.objects.create(id='test_group_1')
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        BusinessGroup.objects.create(id='test_group_2')
        BusinessGroup.objects.create(id='test_group_3')
        bg2 = BusinessGroup.objects.get(id="test_group_2")
        bg3 = BusinessGroup.objects.get(id="test_group_3")
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
        CustomUser.objects.create_user(email='user3@test_group_2.com', password='pass', employee_number='4',
                                       percentage='full_time', business_group=bg2)
        CustomUser.objects.create_user(email='user9@test_group_3.com', password='pass', employee_number='9',
                                       percentage='full_time', business_group=bg3, focal_point=True)
        """creating part time users"""
        CustomUser.objects.create_user(email='user4@test_group_1.com', password='pass', employee_number='5',
                                       percentage='part_time', business_group=bg1)
        CustomUser.objects.create_user(email='user5@test_group_1.com', password='pass', employee_number='6',
                                       percentage='part_time', business_group=bg1)
        CustomUser.objects.create_user(email='user6@test_group_1.com', password='pass', employee_number='7',
                                       percentage='part_time', business_group=bg1)
        CustomUser.objects.create_user(email='user8@test_group_2.com', password='pass', employee_number='8',
                                       percentage='part_time', business_group=bg2, focal_point=True)

    def test_view_assignments_GET(self):
        c = Client()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:assignments'))
        self.assertContains(response, 'You made no assignments yet')
        self.assertContains(response, 'user1@test_group_1.com')
        self.assertContains(response, 'user2@test_group_1.com')
        self.assertContains(response, 'user4@test_group_1.com')
        self.assertNotContains(response, 'user3@test_group_2.com')
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
               {'users': ['user3@test_group_2.com'], 'cubics': ['cubic_test_2']})
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
               {'users': ['user3@test_group_2.com'], 'cubics': ['cubic_test_2']})
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
        user3 = CustomUser.objects.get(email='user3@test_group_2.com')
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
        user3 = CustomUser.objects.get(email='user3@test_group_2.com')
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
        focal_point = CustomUser.objects.get(email='email@example.com')
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
        """part time"""
        user3 = CustomUser.objects.get(email='user3@test_group_2.com')
        user4 = CustomUser.objects.get(email='user4@test_group_1.com')
        user5 = CustomUser.objects.get(email='user5@test_group_1.com')
        response = c.post(reverse('focal_point:delete_all_user_assignments',kwargs={'user_id': user3.id}))
        self.assertEquals(response.status_code,403)
        cubic_test_1 = Cubic.objects.get(id='cubic_test_1')
        cubic_test_5 = Cubic.objects.get(id='cubic_test_5')
        AssignUserCubic.objects.create(assigner=focal_point, assigned_user=user4, cubic=cubic_test_1)
        AssignUserCubic.objects.create(assigner=focal_point, assigned_user=user4, cubic=cubic_test_5)
        AssignUserCubic.objects.create(assigner=focal_point, assigned_user=user5, cubic=cubic_test_1)
        AssignUserCubic.objects.create(assigner=focal_point, assigned_user=user5, cubic=cubic_test_5)
        c.post(reverse('focal_point:delete_all_user_assignments', kwargs={'user_id': user4.id}))
        self.assertFalse(AssignUserCubic.objects.filter(assigned_user=user4).exists())
        self.assertTrue(AssignUserCubic.objects.filter(assigned_user=user5).exists())

    def test_create_request_GET(self):
        focal_point = CustomUser.objects.get(email='email@example.com')
        c = Client()
        c.login(email='user3@test_group_2.com', password='pass')
        response = c.get(reverse('focal_point:createRequest'))
        self.assertEquals(response.status_code, 403)
        c.logout()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:createRequest'))
        self.assertTemplateUsed(response,'focal_point/createrequests.html')
        self.assertContains(response, '<option value="test_group_2">test_group_2</option>')
        self.assertNotContains(response, '<option value="test_group_1">test_group_1</option>')
        self.assertContains(response, '<option value="lab_1">lab_1</option>')

        # TODO : checking dates

    def test_create_request_POST(self):
        focal_point = CustomUser.objects.get(email='email@example.com')
        c = Client()
        c.login(email='user3@test_group_2.com', password='pass')
        response = c.post(reverse('focal_point:createRequest'))
        self.assertEquals(response.status_code, 403)
        c.logout()
        c.login(email='email@example.com', password='pass')
        response = c.post(reverse('focal_point:createRequest'), {'business_group': '', 'full_time_employees_amount': '',
                                                                 'business_group_near_by': '', 'near_lab': '',
                                                                 'part_time_employees_amount': '',
                                                                 'destination_date': ''})
        self.assertContains(response, 'Cant submit empty form')
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        bg2 = BusinessGroup.objects.get(id="test_group_2")
        lab1 = Space.objects.get(id='lab_1', type='Lab')
        c.post(reverse('focal_point:createRequest'), {'business_group': bg1, 'full_time_employees_amount': 1,
                                                             'business_group_near_by': bg2, 'near_lab': lab1,
                                                             'part_time_employees_amount': '', 'destination_date': ''})
        self.assertTrue(FocalPointRequest.objects.filter(business_group=focal_point.business_group,
                                                         business_group_near_by=bg2, near_lab=lab1,
                                                         full_time_employees_amount=1, status='unread').exists())
        c.post(reverse('focal_point:createRequest'), {'business_group': bg1, 'full_time_employees_amount': 1,
                                                             'part_time_employees_amount': 2,
                                                             'business_group_near_by': bg2, 'near_lab': lab1,
                                                             'destination_date': ''})
        self.assertTrue(FocalPointRequest.objects.filter(business_group=focal_point.business_group,
                                                         business_group_near_by=bg2, near_lab=lab1,
                                                         part_time_employees_amount=2,
                                                         full_time_employees_amount=1, status='unread').exists())
        self.assertEquals(2, len(FocalPointRequest.objects.filter(business_group=focal_point.business_group)))

    def test_display_requests_GET(self):
        user2 = CustomUser.objects.get(email='user2@test_group_1.com')
        user3 = CustomUser.objects.get(email='user3@test_group_2.com')
        cubic_test_1 = Cubic.objects.get(id='cubic_test_1')
        cubic_test_3 = Cubic.objects.get(id='cubic_test_3')
        c = Client()
        c.login(email='user3@test_group_2.com', password='pass')
        response = c.get(reverse('focal_point:requests'))
        self.assertEquals(response.status_code, 403)
        c.logout()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:requests'))
        self.assertContains(response, 'No requests yet')
        RequestToChangeCubic.objects.create(user=user2, cubic=cubic_test_1)
        RequestToChangeCubic.objects.create(user=user3, cubic=cubic_test_3)
        response = c.get(reverse('focal_point:requests'))
        self.assertContains(response, 'user2@test_group_1.com')
        self.assertNotContains(response, 'user3@test_group_2.com')

    def test_display_request_GET(self):
        user2 = CustomUser.objects.get(email='user2@test_group_1.com')
        user3 = CustomUser.objects.get(email='user3@test_group_2.com')
        cubic_test_1 = Cubic.objects.get(id='cubic_test_1')
        cubic_test_3 = Cubic.objects.get(id='cubic_test_3')
        c = Client()
        c.login(email='user3@test_group_2.com', password='pass')
        request_1 = RequestToChangeCubic.objects.create(user=user2, cubic=cubic_test_1)
        response = c.get(reverse('focal_point:viewrequest', kwargs={'request_id': request_1.id}))
        self.assertEquals(response.status_code, 403)
        c.logout()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:viewrequest', kwargs={'request_id': request_1.id}))
        self.assertContains(response, 'selected>user2@test_group_1.com</option>')
        self.assertNotContains(response, 'selected>user3@test_group_1.com</option>')
        request_2 = RequestToChangeCubic.objects.create(user=user3, cubic=cubic_test_3)
        response = c.get(reverse('focal_point:viewrequest', kwargs={'request_id': request_2.id}))
        self.assertEquals(response.status_code, 403)

    def test_display_request_POST(self):
        user2 = CustomUser.objects.get(email='user2@test_group_1.com')
        user3 = CustomUser.objects.get(email='user3@test_group_2.com')
        cubic_test_1 = Cubic.objects.get(id='cubic_test_1')
        cubic_test_3 = Cubic.objects.get(id='cubic_test_3')
        cubic_test_5 = Cubic.objects.get(id='cubic_test_5')
        c = Client()
        c.login(email='user3@test_group_2.com', password='pass')
        request_1 = RequestToChangeCubic.objects.create(user=user2, cubic=cubic_test_1)
        response = c.post(reverse('focal_point:viewrequest', kwargs={'request_id': request_1.id}), {'status': 'approved',
                                                                                                    'cubic': cubic_test_1,
                                                                                                    'request_date': str(request_1.request_date).split(' ')[0],
                                                                                                    'reason':'',
                                                                                                    'user':user2,
                                                                                                   'notes': 'read'})
        self.assertEquals(response.status_code, 403)
        self.assertFalse(RequestToChangeCubic.objects.filter(user=user2, cubic=cubic_test_1, notes="read",
                                                             status="approved").exists())
        c.logout()
        c.login(email='email@example.com', password='pass')
        response = c.post(reverse('focal_point:viewrequest', kwargs={'request_id': request_1.id}), {'user': user2,
                                                                                         'cubic': cubic_test_1,
                                                                                         'status': "approved",
                                                                                         'notes': "read",
                                                                                         'request_date': str(request_1.request_date).split(' ')[0],
                                                                                         'reason': ''
                                                                                         })
        self.assertTrue(RequestToChangeCubic.objects.filter(user=user2, cubic=cubic_test_1, notes='read',
                                                            status='approved').exists())
        c.post(reverse('focal_point:viewrequest', kwargs={'request_id': request_1.id}), {'user':user2,
                                                                                         'request_date':  str(request_1.request_date).split(' ')[0],
                                                                                         'reason': '',
                                                                                         'status': 'approved',
                                                                                         'notes': 'already approved'})
        self.assertTrue(
            RequestToChangeCubic.objects.filter(user=user2, cubic=cubic_test_1, notes='already approved',
                                                status='approved').exists())
        request_3 = RequestToChangeCubic.objects.create(user=user2)
        c.post(reverse('focal_point:viewrequest', kwargs={'request_id': request_3.id}), {'status': 'unread',
                                                                                         'user': user2,
                                                                                         'request_date': str(
                                                                                             request_3.request_date).split(
                                                                                             ' ')[0],
                                                                                         'notes': '',
                                                                                         'reason': 'too small',
                                                                                         })
        self.assertTrue(
            RequestToChangeCubic.objects.filter(user=user2, notes='', status='unread',reason='too small').exists())
        request_4 = RequestToChangeCubic.objects.create(user=user2)
        c.post(reverse('focal_point:viewrequest', kwargs={'request_id': request_4.id}), {'status': 'unread',
                                                                                         'user':user2,
                                                                                         'request_date':str(request_4.request_date).split(' ')[0],
                                                                                         'notes': '',
                                                                                         'reason': '',
                                                                                         })
        self.assertEquals(len(RequestToChangeCubic.objects.filter(user=user2)),3)
        request_2 = RequestToChangeCubic.objects.create(user=user3, cubic=cubic_test_3)
        response = c.post(reverse('focal_point:viewrequest', kwargs={'request_id': request_2.id}), {'status': 'approved',
                                                                                                    'user': user3,
                                                                                                    'request_date': str(
                                                                                                        request_2.request_date).split(
                                                                                                        ' ')[0],
                                                                                                    'cubic': cubic_test_3,
                                                                                                    'notes': 'read'})
        self.assertEquals(response.status_code, 403)

    def test_display_my_requests_GET(self):
        focal_point = CustomUser.objects.get(email='email@example.com')
        bg2 = BusinessGroup.objects.get(id="test_group_2")
        c = Client()
        c.login(email='user3@test_group_2.com', password='pass')
        response = c.get(reverse('focal_point:myrequests'))
        self.assertEquals(response.status_code, 403)
        c.logout()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:myrequests'))
        self.assertTemplateUsed(response, 'focal_point/myrequests.html')
        self.assertContains(response,'You have not sent any requests yet.')
        FocalPointRequest.objects.create(business_group=focal_point.business_group,full_time_employees_amount=1,
                                         business_group_near_by=bg2)
        FocalPointRequest.objects.create(business_group=focal_point.business_group, part_time_employees_amount=1,status='approved')
        response = c.get(reverse('focal_point:myrequests'))
        self.assertContains(response, 'Status: unread')
        self.assertContains(response, 'Status: approved')

    def test_display_my_request_GET(self):
        focal_point_bg_1 = CustomUser.objects.get(email='email@example.com')
        focal_point_bg_2 = CustomUser.objects.get(email='user8@test_group_2.com')
        bg2 = BusinessGroup.objects.get(id="test_group_2")
        c = Client()
        focalrequest1 = FocalPointRequest.objects.create(business_group=focal_point_bg_1.business_group, full_time_employees_amount=1,
                                         business_group_near_by=bg2)
        focalrequest2 = FocalPointRequest.objects.create(business_group=focal_point_bg_2.business_group, part_time_employees_amount=1,
                                         status='approved')
        c.login(email='user3@test_group_2.com', password='pass')
        response = c.get(reverse('focal_point:viewmyrequest',kwargs={'request_id': focalrequest2.id}))
        self.assertEquals(response.status_code, 403)
        response = c.get(reverse('focal_point:viewmyrequest', kwargs={'request_id': focalrequest1.id}))
        self.assertEquals(response.status_code, 403)
        c.logout()
        c.login(email='user8@test_group_2.com', password='pass')
        response = c.get(reverse('focal_point:viewmyrequest', kwargs={'request_id': focalrequest2.id}))
        self.assertTemplateUsed(response, 'focal_point/viewrequest.html')
        response = c.get(reverse('focal_point:viewmyrequest', kwargs={'request_id': focalrequest1.id}))
        self.assertEquals(response.status_code, 403)
        c.logout()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:viewmyrequest', kwargs={'request_id': focalrequest1.id}))
        self.assertContains(response, '<option value="test_group_2" selected>test_group_2</option>')
        self.assertContains(response, '<option value="" selected>---------</option>')

    def test_display_my_request_POST(self):
        # business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE, related_name='+')
        # full_time_employees_amount = models.PositiveIntegerField(blank=True, null=True)
        # part_time_employees_amount = models.PositiveIntegerField(blank=True, null=True)
        # business_group_near_by = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE, related_name='+',
        #                                            blank=True, null=True)
        # near_lab = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
        # # near_conference_room = models.BooleanField(default=False)
        # date = models.DateField(default=now())
        # destination_date = models.DateField(null=True, blank=True)
        # status = models.CharField(max_length=MAX_LENGTH, choices=(('unread', 'unread'), ('in progress', 'in progress'),
        #                                                           ('approved', 'approved'), ('denied', 'denied')),
        #                           default='unread')
        # notes = models.TextField(blank=True)
        focal_point_bg_1 = CustomUser.objects.get(email='email@example.com')
        focal_point_bg_2 = CustomUser.objects.get(email='user8@test_group_2.com')
        bg2 = BusinessGroup.objects.get(id="test_group_2")
        bg3 = BusinessGroup.objects.get(id="test_group_3")
        lab1 = Space.objects.get(id='lab_1')
        c = Client()
        focalrequest1 = FocalPointRequest.objects.create(business_group=focal_point_bg_1.business_group,
                                                         full_time_employees_amount=1,
                                                         business_group_near_by=bg2)
        focalrequest2 = FocalPointRequest.objects.create(business_group=focal_point_bg_2.business_group,
                                                         part_time_employees_amount=1)
        c.login(email='user3@test_group_2.com', password='pass')
        response = c.post(reverse('focal_point:viewmyrequest', kwargs={'request_id': focalrequest2.id}),
                          {'full_time_employees_amount': '','part_time_employees_amount': '1'})
        self.assertEquals(response.status_code, 403)
        response = c.post(reverse('focal_point:viewmyrequest', kwargs={'request_id': focalrequest1.id}),
                          {'full_time_employees_amount': '1',
                           'part_time_employees_amount': '', 'business_group_near_by': bg2})
        self.assertEquals(response.status_code, 403)
        c.logout()
        c.login(email='email@example.com', password='pass')
        c.post(reverse('focal_point:viewmyrequest', kwargs={'request_id': focalrequest1.id}),
               {'full_time_employees_amount': 1, 'part_time_employees_amount': '', 'business_group_near_by': bg3,
                'near_lab': '', 'destination_date': ''})
        self.assertEqual(len(FocalPointRequest.objects.filter(business_group=focal_point_bg_1.business_group)), 1)
        self.assertTrue(FocalPointRequest.objects.filter(business_group=focal_point_bg_1.business_group,
                                                         full_time_employees_amount=1, business_group_near_by=bg3))
        c.post(reverse('focal_point:viewmyrequest', kwargs={'request_id': focalrequest1.id}),
               {'full_time_employees_amount':'', 'part_time_employees_amount': '1', 'business_group_near_by': bg3,
                'near_lab': '', 'destination_date': ''})
        self.assertEqual(len(FocalPointRequest.objects.filter(business_group=focal_point_bg_1.business_group)), 1)
        self.assertTrue(FocalPointRequest.objects.filter(business_group=focal_point_bg_1.business_group,
                                                         part_time_employees_amount=1,
                                                         business_group_near_by=bg3).exists())
        self.assertTrue(FocalPointRequest.objects.get(business_group=focal_point_bg_1.business_group,
                                                      part_time_employees_amount=1,
                                                      business_group_near_by=bg3).full_time_employees_amount!=1)
        c.post(reverse('focal_point:viewmyrequest', kwargs={'request_id': focalrequest1.id}),
               {'full_time_employees_amount': '', 'part_time_employees_amount': '1', 'business_group_near_by': bg3,
                'near_lab': lab1, 'destination_date': ''})
        self.assertEqual(len(FocalPointRequest.objects.filter(business_group=focal_point_bg_1.business_group)), 1)
        self.assertTrue(FocalPointRequest.objects.filter(business_group=focal_point_bg_1.business_group,
                                                         part_time_employees_amount=1,
                                                         business_group_near_by=bg3,near_lab=lab1).exists())
        self.assertTrue(FocalPointRequest.objects.get(business_group=focal_point_bg_1.business_group,
                                                      part_time_employees_amount=1,near_lab=lab1,
                                                      business_group_near_by=bg3).full_time_employees_amount != 1)
        c.post(reverse('focal_point:viewmyrequest', kwargs={'request_id': focalrequest1.id}),
               {'full_time_employees_amount': '', 'part_time_employees_amount': '1', 'business_group_near_by': bg3,
                'near_lab': lab1,'destination_date': str(datetime.now()).split(' ')[0]})
        self.assertEqual(len(FocalPointRequest.objects.filter(business_group=focal_point_bg_1.business_group)), 1)
        self.assertTrue(FocalPointRequest.objects.filter(business_group=focal_point_bg_1.business_group,
                                                         part_time_employees_amount=1,
                                                         business_group_near_by=bg3, near_lab=lab1,destination_date=datetime.now()).exists())
        self.assertTrue(FocalPointRequest.objects.get(business_group=focal_point_bg_1.business_group,
                                                      part_time_employees_amount=1,
                                                      business_group_near_by=bg3, near_lab=lab1,
                                                      destination_date=datetime.now()).full_time_employees_amount != 1)
        self.assertEquals(FocalPointRequest.objects.get(business_group=focal_point_bg_1.business_group,
                                                        part_time_employees_amount=1,
                                                        business_group_near_by=bg3, near_lab=lab1,
                                                        destination_date=datetime.now()).full_time_employees_amount,None)

    def test_delete_request_POST(self):
        focal_point_bg_1 = CustomUser.objects.get(email='email@example.com')
        focal_point_bg_2 = CustomUser.objects.get(email='user8@test_group_2.com')
        bg2 = BusinessGroup.objects.get(id="test_group_2")
        lab1 = Space.objects.get(id='lab_1')
        c = Client()
        focalrequest1_1 = FocalPointRequest.objects.create(business_group=focal_point_bg_1.business_group,
                                                         full_time_employees_amount=1,
                                                         business_group_near_by=bg2)
        focalrequest1_2 = FocalPointRequest.objects.create(business_group=focal_point_bg_1.business_group,
                                                           full_time_employees_amount=1,
                                                          near_lab=lab1)
        focalrequest2 = FocalPointRequest.objects.create(business_group=focal_point_bg_2.business_group,
                                                         part_time_employees_amount=1,
                                                         status='approved')
        c.login(email='user3@test_group_2.com', password='pass')
        response = c.post(reverse('focal_point:deleterequest', kwargs={'request_id': focalrequest2.id}))
        self.assertEquals(response.status_code, 403)
        response = c.post(reverse('focal_point:deleterequest', kwargs={'request_id': focalrequest1_1.id}))
        self.assertEquals(response.status_code, 403)
        c.logout()
        c.login(email='user8@test_group_2.com', password='pass')
        response = c.post(reverse('focal_point:deleterequest', kwargs={'request_id': focalrequest2.id}))
        self.assertFalse(FocalPointRequest.objects.filter(id=focalrequest2.id).exists())
        response = c.post(reverse('focal_point:deleterequest', kwargs={'request_id': focalrequest1_1.id}))
        self.assertEquals(response.status_code, 403)
        self.assertTrue(FocalPointRequest.objects.filter(id=focalrequest1_1.id).exists())
        c.logout()
        c.login(email='email@example.com', password='pass')
        response = c.post(reverse('focal_point:deleterequest', kwargs={'request_id': focalrequest1_1.id}))
        self.assertRedirects(response,'/focal_point/myrequests/')
        self.assertFalse(FocalPointRequest.objects.filter(id=focalrequest1_1.id).exists())
        self.assertTrue(FocalPointRequest.objects.filter(id=focalrequest1_2.id).exists())
        response = c.post(reverse('focal_point:deleterequest', kwargs={'request_id': focalrequest1_2.id}))
        self.assertRedirects(response, '/focal_point/myrequests/')
        self.assertFalse(FocalPointRequest.objects.filter(business_group=focal_point_bg_1.business_group).exists())

    def test_display_new_positions_GET(self):
        focal_point_bg_1 = CustomUser.objects.get(email='email@example.com')
        focal_point_bg_2 = CustomUser.objects.get(email='user8@test_group_2.com')
        focal_point_bg_3 = CustomUser.objects.get(email='user9@test_group_3.com')
        bg1 = BusinessGroup.objects.get(id="test_group_1")
        bg2 = BusinessGroup.objects.get(id="test_group_2")
        position_bg_1_1 = NewPosition.objects.create(percentage='full_time', business_group=bg1)
        position_bg_1_2 = NewPosition.objects.create(percentage='part_time', business_group=bg1)
        position_bg_2_1 = NewPosition.objects.create(name='new position', percentage='full_time', business_group=bg2)
        c = Client()
        c.login(email='user9@test_group_3.com', password='pass')
        response = c.get(reverse('focal_point:newpositions'))
        self.assertContains(response,'There are no open positions for the group at the moment')
        c.logout()
        c.login(email='user8@test_group_2.com', password='pass')
        response = c.get(reverse('focal_point:newpositions'))
        self.assertContains(response,'Percentage: full_time')
        c.logout()
        c.login(email='email@example.com', password='pass')
        response = c.get(reverse('focal_point:newpositions'))
        self.assertContains(response, 'Percentage: full_time')
        self.assertContains(response, 'Percentage: part_time')
        c.login(email='user3@test_group_2.com', password='pass')
        response = c.get(reverse('focal_point:newpositions'))
        self.assertEquals(response.status_code,403)



