import os
from pathlib import Path
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .user_factory import UserFactory
from .profile_factory import ProfileFactory
from ..views import ShowCorrelation
from core.models import Report
from users.models import Profile
from .testdata import html_test_response_table
from django.contrib.auth.models import User

current_file_path = Path(__file__).resolve()


class ShowCorrelationViewTest(TestCase):
    def setUp(self) -> None:
        self.password = "Xyz12234"
        self.profile: Profile = ProfileFactory.create()

    def test_profile_creation(self):
        # Use the ProfileFactory to create a user

        # Check if the user's username and password are correct
        self.assertIsNotNone(
            self.profile.user.username, msg="Username should not be empty"
        )
        self.assertIsNotNone(self.password, msg="Password should not be empty")

        # You can also check other attributes of the user and self.profile objects if needed
        self.assertEqual(
            self.profile.occupation, "Lawyer", msg="Occupation should be 'Lawyer'"
        )
        # Add more assertions as needed based on the fields in the self.profile model.

        # (Optional) Check that the user object is saved to the database
        self.assertTrue(
            self.profile.user.pk, msg="User should be saved to the database"
        )

        # (Optional) Check that the user's password is hashed
        self.assertTrue(
            self.profile.user.has_usable_password(),
            msg="User password should be hashed",
        )

    def test_show_correlation(self):
        # Create an authorized user

        # Log in the user
        self.client.login(username=self.profile.user.username, password=self.password)

        # Define the file path and open the file
        file_path = os.path.join(
            current_file_path.parent.parent, "testfiles", "test.xlsx"
        )

        with open(file_path, "rb") as file:
            # Create a SimpleUploadedFile from the file
            uploaded_file = SimpleUploadedFile(
                "text.xlsx",
                file.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

            # Make a POST request to the view with the uploaded file and other form data
            response = self.client.post(
                reverse("correlate"),
                {
                    "excel_file": uploaded_file,
                    "pearson": "on",
                    "low": "on",
                    "title": "Testing",
                },
            )

            expected_low_result = html_test_response_table
            # Assert that the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

        # Assert that a Report object has been created with the correct attributes
        report: Report = Report.objects.get(title="Testing")
        self.assertEqual(report.correlaton_type, "pearson")
        self.assertEqual(report.low_correlaton_result, expected_low_result)
        self.assertEqual(
            report.high_correlaton_result, "High correlation range has not been chosen"
        )
        self.assertEqual(report.author, self.profile.user)
