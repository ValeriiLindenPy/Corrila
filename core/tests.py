import os
from pathlib import Path

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from .views import ShowCorrelation
from .models import Report

current_file_path = Path(__file__).resolve()




class ShowCorrelationViewTest(TestCase):
    def test_show_correlation(self):
        # Create an authorized user
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Define the file path and open the file
        file_path = os.path.join(current_file_path.parent, 'testfiles', 'test.xlsx')

        with open(file_path, 'rb') as file:
            # Create a SimpleUploadedFile from the file
            uploaded_file = SimpleUploadedFile('text.xlsx', file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            # Make a POST request to the view with the uploaded file and other form data
            response = self.client.post(reverse('correlate'), {
                'excel_file': uploaded_file,
                'pearson': 'on',
                'low': 'on',
                'title': 'Test Report'
            })
            
        
            expected_low_result = '''<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AV</th>
      <th>Moisture</th>
      <th>AI</th>
      <th>VIS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Moisture</th>
      <td>-0.013851</td>
      <td>NaN</td>
      <td>-0.083166</td>
      <td>-0.309723</td>
    </tr>
    <tr>
      <th>AI</th>
      <td>-0.367713</td>
      <td>-0.083166</td>
      <td>NaN</td>
      <td>-0.274727</td>
    </tr>
    <tr>
      <th>VIS</th>
      <td>0.489082</td>
      <td>-0.309723</td>
      <td>-0.274727</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>AV</th>
      <td>NaN</td>
      <td>-0.013851</td>
      <td>-0.367713</td>
      <td>0.489082</td>
    </tr>
  </tbody>
</table>'''    

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that a Report object has been created with the correct attributes
        report = Report.objects.get(title='Test Report')
        self.assertEqual(report.correlaton_type, 'pearson')
        self.assertEqual(report.low_correlaton_result, expected_low_result)
        self.assertEqual(report.high_correlaton_result, 'High correlation range has not been chosen')
        self.assertEqual(report.author, user)




