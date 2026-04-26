from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from .models import DetectionTask


class AuthApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="demo_user",
            email="demo@example.com",
            password="demo-pass-123",
        )

    def test_login_returns_jwt_tokens(self):
        response = self.client.post(
            "/api/login/",
            {"username": "demo@example.com", "password": "demo-pass-123"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


class TaskApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="task_user",
            email="task@example.com",
            password="task-pass-123",
        )

    def test_tasks_list_returns_current_user_tasks(self):
        self.client.force_authenticate(self.user)
        upload = SimpleUploadedFile("task.jpg", b"fake-jpg-bytes", content_type="image/jpeg")
        DetectionTask.objects.create(
            task_name="demo-task",
            task_type="image",
            file_path=upload,
            created_by=self.user,
            status="pending",
        )

        response = self.client.get("/api/detection/tasks")

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "demo-task")

    @patch("detection.views.threading.Thread")
    def test_upload_endpoint_creates_task(self, mock_thread):
        self.client.force_authenticate(self.user)
        mock_thread.return_value.start.return_value = None
        upload = SimpleUploadedFile("upload.jpg", b"fake-jpg-bytes", content_type="image/jpeg")

        response = self.client.post(
            "/api/detection/upload",
            {"taskName": "upload-task", "confidence": "0.6", "files": [upload]},
            format="multipart",
        )

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data.get("code"), 200)
        self.assertTrue(
            DetectionTask.objects.filter(task_name="upload-task", created_by=self.user).exists()
        )
