from datetime import datetime

from django.db.models import Count
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.views.generic import View

from .forms import DatePickerForm
from .models import ChatMessage


# Create your views here.


def user_message_view(request):
    data = {}
    date = request.GET.get('date', None)
    if date:
        date_format = '%d/%m/%Y %H:%M'
        date_object = datetime.strptime(date, date_format)

        # Make datetime object timezone aware
        date_object = make_aware(date_object)

        data = ChatMessage.objects.filter(created_at__date=date_object).values(
            'user__first_name', 'user__username'
        ).annotate(msg_cnt=Count('id'))

    form = DatePickerForm()

    print(request.GET.get('date'))

    # Return a "created" (201) response code.
    return render(request, 'index.html', {'form': form, 'data': data})