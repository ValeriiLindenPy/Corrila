from corrila.celery import app
from .utils import *
from .models import Report, User, TemporaryFile

from django.core.exceptions import ObjectDoesNotExist

@app.task
def correlate_async(content):
    try:
        file_object = TemporaryFile.objects.get(pk=content['file_id'])
        correlator = CorrelationTools()
        correlator.filter_low_high_corr(file_object.file, method_chosen=content['correlaton_type'])
        user = User.objects.get(pk=content['author'])
        if content['low_choice']:
            low = correlator.get_low_corr()
        else:
            low = "Low correlation range has not been chosen"

        if content['high_choice']:
            high = correlator.get_high_corr()
        else:
            high = "High correlation range has not been chosen"

        Report.objects.create(
            title=content['title'],
            low_correlaton_result=low,
            high_correlaton_result=high,
            correlaton_type=content['correlaton_type'],
            author=user
        )
        file_object.delete()
    except ObjectDoesNotExist:
        # Handle the case when the TemporaryFile object doesn't exist
        Report.objects.create(
            title=content['title'],
            low_correlaton_result= 'Presented data is incorrect or file missing',
            high_correlaton_result='Presented data is incorrect or file missing',
            correlaton_type=content['correlaton_type'],
            author=user
        )
        pass