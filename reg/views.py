from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Positions
from .models import Vacation
from .models import Worker

User = get_user_model()


def bad_page(request):
    return render(request, 'reg/regUNSUCCESS.html')


def bad_auth(request):
    return render(request, 'reg/authUNSUCCESS.html')


def suc_registration(request):
    return render(request, 'reg/regSUCCESS.html')


def select(request):
    return render(request, 'reg/selectREG_AUTH.html')


def auth(request):
    if request.method == 'POST':
        username = request.POST['phone_number']
        password = request.POST['psw']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("select_accept_order"))
        else:
            return HttpResponseRedirect(reverse("bad_auth"))

    return render(request, 'reg/indexAUTH.html')


@login_required(login_url='/auth/')
def search_worker_for_vacations(request):
    if request.method == "POST":
        phone_number = request.POST['phone_number']
        print(phone_number)
        try:
            worker_id_search = Worker.objects.get(phone_number=phone_number).id
            print(worker_id_search)
            return HttpResponseRedirect(reverse("vacations_for_worker", args=(worker_id_search,)))
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse('worker_search_err'))

    return render(request, 'reg/workerSEARCHVacation.html')


@login_required(login_url='/auth/')
def vacations_for_worker(request, worker_id):
    if request.method == "POST":
        start_date = request.POST['date_start']
        end_date = request.POST['date_end']

        vacation = Vacation()

        try:
            vacation.date_start = start_date
            vacation.date_end = end_date
            vacation.worker_id = worker_id
            vacation.save()
            return HttpResponseRedirect(reverse('worker_vacation_success'))
        except Exception:
            return HttpResponseRedirect(reverse('worker_vacation_err'))

    return render(request, 'reg/workerVACATION.html')


@login_required(login_url='/auth/')
def worker_search_err(request):
    return render(request, 'reg/workerSEARCHErr.html')


@login_required(login_url='/auth/')
def worker_vacation_err(request):
    return render(request, 'reg/workerVACATIONErr.html')


@login_required(login_url='/auth/')
def worker_vacation_success(request):
    return render(request, 'reg/workerVACATIONSuc.html')


@login_required(login_url='/auth/')
def test(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def index(request):
    position = Positions.objects.all()
    position_list = [i.name for i in position]
    worker_objects = Worker.objects.all()

    if request.method == 'POST':
        first_name = request.POST['fname']
        second_name = request.POST['sname']
        third_name = request.POST['tname']
        address = request.POST['addr']
        phone_number = request.POST['PhoneNumber']
        pleases = request.POST['pleases']
        password = request.POST['psw']

        phone_number_list = [i.phone_number for i in worker_objects]

        for item in phone_number_list:
            if item == phone_number:
                return HttpResponseRedirect(reverse("bad_page"))

        obj = User.objects.create_user(phone_number=phone_number, password=password)
        obj.first_name = first_name
        obj.second_name = second_name
        obj.third_name = third_name
        obj.address_name = address
        obj.phone_number = phone_number
        obj.positions_id = Positions.objects.get(name=pleases).id
        obj.save()

        return HttpResponseRedirect(reverse("suc_registration"))

    context = {
        'list': position_list
    }

    return render(request, 'reg/indexREG.html', context)
# Create your views here.
