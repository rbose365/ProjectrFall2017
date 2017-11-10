from projectr import views
from django.test import TestCase
from models import Project, Message, Bid, Section, Notification, Question, InstructorKey, Tag
import mock

class TestRegister(TestCase):

	def test_register_student_authenticated(self):

		# Create a mock user
		mockUser = mock.Mock()
		mockUser.is_authenticated.return_value = True
		mockUser.profile.user_type = 'S'

		# Create a mock request
		mockReq = mock.Mock()
		mockReq.method = "POST"
		mockReq.user = mockUser
		
		assert "student" in str(views.register(mockReq)['Location'])

	def test_register_teacher_authenticated(self):

		# Create a mock user
		mockUser = mock.Mock()
		mockUser.is_authenticated.return_value = True
		mockUser.profile.user_type = 'I'

		# Create a mock request
		mockReq = mock.Mock()
		mockReq.method = "POST"
		mockReq.user = mockUser
		
		assert "instructor" in str(views.register(mockReq)['Location'])

	def test_register_client_authenticated(self):

		# Create a mock user
		mockUser = mock.Mock()
		mockUser.is_authenticated.return_value = True
		mockUser.profile.user_type = 'C'

		# Create a mock request
		mockReq = mock.Mock()
		mockReq.method = "POST"
		mockReq.user = mockUser
		
		assert "client" in str(views.register(mockReq)['Location'])