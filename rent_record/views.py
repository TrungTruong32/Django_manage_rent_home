from django.shortcuts import render, redirect
from .models import RentRecord
from .forms import RentRecordForm

def home(request):
    records = RentRecord.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'records': records})

def add_record(request):
    if request.method == 'POST':
        form = RentRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RentRecordForm()
    return render(request, 'add_record.html', {'form': form})
