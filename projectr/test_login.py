from projectr import views
from django.test import TestCase
from models import Project, Message, Bid, Section, Notification, Question, InstructorKey, Tag
import mock

class TestLogin(TestCase):

	def test_login_student_authenticated(self):

		# Create a mock user
		mockUser = mock.Mock()
		mockUser.is_authenticated.return_value = True
		mockUser.profile.user_type = 'S'

		# Create a mock login request
		mockReq = mock.Mock()
		mockReq.method = "POST"
		mockReq.user = mockUser

		assert "student" in str(views.login_view(mockReq)['Location'])

	def test_login_teacher_authenticated(self):

		# Create a mock user
		mockUser = mock.Mock()
		mockUser.is_authenticated.return_value = True
		mockUser.profile.user_type = 'I'

		# Create a mock login request
		mockReq = mock.Mock()
		mockReq.method = "POST"
		mockReq.user = mockUser

		assert "instructor" in str(views.login_view(mockReq)['Location'])

	def test_login_client_authenticated(self):

		# Create a mock user
		mockUser = mock.Mock()
		mockUser.is_authenticated.return_value = True
		mockUser.profile.user_type = 'C'

		# Create a mock login request
		mockReq = mock.Mock()
		mockReq.method = "POST"
		mockReq.user = mockUser

		assert "client" in str(views.login_view(mockReq)['Location'])