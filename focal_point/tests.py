from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import get_object_or_404


class CustomUserTestCase(TestCase):
    def setUp(self):
        pass

    def test_view_assignments_GET(self):
        pass

    def test_assign_part_time_GET(self):
        pass

    def test_assign_part_time_POST(self):
        pass

    def test_assign_full_time_GET(self):
        pass

    def test_assign_full_time_POST(self):
        pass

    def test_edit_assignments_for_user_GET(self):
        pass

    def test_edit_assignments_for_user_POST(self):
        pass

    def test_view_all_user_assignments_GET(self):
        pass

    def test_delete_all_user_assignments_POST(self):
        pass

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
