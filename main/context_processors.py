from django.conf import settings
from .models import *

context_processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

def display_bill_length(request):
    try:
        if request.user.is_authenticated:
            bill_length = Bill.objects.get(
                user = request.user, charged=False).items.all().count
            return {
                'bill_length': bill_length
            }
        else:
            return{
                'bill_length': 0
            }
    except Bill.DoesNotExist:
        return {
            'bill_length': 0
        }


context_processors.append(
    'main.context_processors.display_bill_lengt'
)
