from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Company
from .forms import UploadFileForm, QueryForm
import csv
import io

def login_view(request):
    return render(request, 'account/login.html')

@login_required
def upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                return render(request, 'upload.html', {'form': form, 'error': 'File is not CSV type'})
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                _, created = Company.objects.update_or_create(
                    id=column[0],
                    defaults={
                        'name': column[1],
                        'address': column[2],
                        'city': column[3],
                        'state': column[4],
                        'zip_code': column[5],
                    }
                )
            return redirect('query_builder')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def query_builder_view(request):
    form = QueryForm()
    count = None
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM core_company WHERE city = %s AND state = %s", [city, state])
                count = cursor.fetchone()[0]
    return render(request, 'query_builder.html', {'form': form, 'count': count})
