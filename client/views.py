from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from hotel_numbers.models import HotelNumber, NumberType
from reg.models import Worker, Positions, Vacation
from .models import Client, Order, BlackList, ServiceList, AdditionalOrder, MenuList


def search_err(request):
    return render(request, 'client/orderSEARCHErr.html')


def client_select(request):
    return render(request, 'client/selectORDER_ACCEPT.html')


def order_success(request):
    return render(request, 'client/orderSUCCESS.html')


def client_out_search(request):
    if request.method == "POST":
        passport = request.POST['passport_number']
        try:
            client_id_search = Client.objects.get(passport_field=passport).id
            # print(client_id_search)
            return HttpResponseRedirect(reverse("client_out", args=(client_id_search,)))
        except Exception:
            return HttpResponseRedirect(reverse("client_out_search_err"))

    return render(request, 'client/clientOUTSERCH.html')


def client_out_search_err(request):
    return render(request, 'client/clientOUTSERCErr.html')


def client_out_suc(request):
    return render(request, 'client/clientOUTSERCHSuc.html')


def client_out_err(request):
    return render(request, 'client/clientOUTErr.html')


def client_out(request, client_id):
    client: Client = Client.objects.filter(id=client_id).first()

    f_name = client.first_name
    s_name = client.second_name
    t_name = client.third_name

    order: Order = Order.objects.filter(execution=True, executed=False, client_id=client_id).first()

    try:
        date_in = order.check_in_date
        date_out = order.check_out_date
    except Exception:
        return HttpResponseRedirect(reverse("client_out_err"))

    client_number = order.number_id
    number: HotelNumber = HotelNumber.objects.filter(id=client_number).first()

    worker_id = number.worker_id

    worker: Worker = Worker.objects.filter(id=worker_id).first()

    w_f_name = worker.first_name
    w_s_name = worker.second_name

    try:
        if request.method == 'POST':
            number.room_condition = False
            number.room_occupancy = False
            number.save()

            order.execution = False
            order.executed = True
            order.save()

            return HttpResponseRedirect(reverse("client_out_suc"))
    except Exception:
        return HttpResponseRedirect(reverse("client_out_err"))

    context = {
        'f_name': f_name,
        's_name': s_name,
        't_name': t_name,
        'date_in': date_in,
        'date_out': date_out,
        'w_f_name': w_f_name,
        'w_s_name': w_s_name
    }

    return render(request, 'client/clientOUT.html', context)


def black_list_info(request, client_id):
    bad_client: BlackList = BlackList.objects.filter(client_id=client_id).first()

    case_date = bad_client.case_date
    time_out_date = bad_client.time_out_date
    reason = bad_client.reason

    context = {
        'case_date': case_date,
        'time_out': time_out_date,
        'reason': reason
    }
    return render(request, 'client/blacklistINFO.html', context)


def black_list_err(request, client):
    if request.method == 'POST':
        client_id = client
        return HttpResponseRedirect(reverse("black_list_add", args=(client_id,)))
    return render(request, 'client/blacklistERR.html')


def black_list_add(request, client_id):
    if request.method == 'POST':
        case_date = request.POST['case_date']
        date_out = request.POST['date_out']
        reason = request.POST['reason']

        bad_client = BlackList()

        bad_client.case_date = case_date
        bad_client.time_out_date = date_out
        bad_client.reason = reason
        bad_client.client_id = client_id

        bad_client.save()

        return HttpResponseRedirect(reverse("black_list_info", args=(client_id,)))

    return render(request, 'client/blacklistADD.html')


def black_list(request):
    if request.method == "POST":
        passport = request.POST['passport_number']
        client = Client.objects.get(passport_field=passport).id
        bad_client = BlackList.objects.all()

        if not bad_client:
            print(client)
            return HttpResponseRedirect(reverse("black_list_err", args=(client,)))
        else:
            for i in bad_client:
                print(i.client_id, client)
                if i.client_id == client:
                    return HttpResponseRedirect(reverse("black_list_info", args=(client,)))

        return HttpResponseRedirect(reverse("black_list_err", args=(client,)))

    return render(request, 'client/blacklistSEARCH.html')


def additional_order_search(request):
    if request.method == "POST":
        passport = request.POST['passport_number']
        try:
            client_id_search = Client.objects.get(passport_field=passport).id
            # print(client_id_search)
            return HttpResponseRedirect(reverse("additional_order", args=(client_id_search,)))
        except Exception:
            return HttpResponseRedirect(reverse("additional_search_err"))

    return render(request, 'client/additional_orderSEARCHING.html')


def additional_order(request, client_id):
    client: Client = Client.objects.filter(id=client_id).first()

    f_name = client.first_name
    s_name = client.second_name
    t_name = client.third_name

    vacation = Vacation.objects.all()

    service_list = ServiceList.objects.all()

    worker: Worker = Worker.objects.filter(positions_id=Positions.objects.filter(name='Разносчик').first().id)

    workers = list(worker)

    vacation_filter_for_worker = list(filter(lambda x: not vacation.filter(worker_id=x.id), workers))

    if request.method == 'POST':
        try:
            date = request.POST.get('Addition_date', '')
            coast = request.POST.get('Addition_coast', 0)
            additional = request.POST.get('Additional', None)
            worker = request.POST['Worker']

            print(date, coast, additional, worker)
            menu: MenuList = MenuList.objects.all().last()
            add_list = AdditionalOrder()

            add_list.order_date = date
            add_list.coast = coast
            add_list.client_id = client_id
            add_list.Menu_id = menu.id
            add_list.service_id = additional
            add_list.worker_id = worker

            add_list.save()

            if additional == '1':
                order: Order = Order.objects.filter(client_id=client_id).first()
                number_id = order.number_id
                print(number_id)
                number: HotelNumber = HotelNumber.objects.filter(id=number_id).first()
                number.room_condition = False
                number.save()
            return HttpResponseRedirect(reverse("additional_order_success", args=(client_id,)))
        except Exception:
            return HttpResponseRedirect(reverse("additional_err"))

    context = {
        'f_name': f_name,
        's_name': s_name,
        't_name': t_name,
        'worker': vacation_filter_for_worker,
        'service_list': service_list
    }

    return render(request, 'client/additional_order.html', context)


def additional_search_err(request):
    return render(request, 'client/additional_SEARCHErr.html')


def additional_order_success(request, client_id):
    context = {
        'client_id': client_id
    }
    return render(request, 'client/additional_SUCCESS.html', context)


def additional_err(request):
    return render(request, 'client/additional_err.html')


def cleaning_room_err(request):
    return render(request, 'client/numberCLININGErr.html')


def cleaning_room(request):
    room_mass = []
    item = HotelNumber.objects.all()

    for i in item:
        if i.room_condition is False:
            room_mass.append({
                'numb_id': i.id,
                'worker': Worker.objects.filter(id=i.worker_id).first()
            })

    if request.method == 'POST':
        try:
            number_id = request.POST['Number']
            number: HotelNumber = HotelNumber.objects.filter(id=number_id).first()
            number.room_condition = True
            number.worker_id = None
            number.save()

            return HttpResponseRedirect(reverse("cleaning_room"))
        except Exception:
            return HttpResponseRedirect(reverse("cleaning_room_err"))

    context = {
        'hotel_numbers': room_mass,
    }

    return render(request, 'client/numberCLINING.html', context)


def order_search(request):
    if request.method == "POST":
        passport = request.POST['passport_number']
        try:
            client_id_search = Client.objects.get(passport_field=passport).id
            # print(client_id_search)
            return HttpResponseRedirect(reverse("order_accept", args=(client_id_search,)))
        except Exception:
            return HttpResponseRedirect(reverse("search_err"))

    return render(request, 'client/orderSEARCHING.html')


def order_accept(request, client_id):
    client: Client = Client.objects.filter(id=client_id).first()

    f_name = client.first_name
    s_name = client.second_name
    t_name = client.third_name
    passport = client.passport_field

    order: Order = Order.objects.filter(execution=False, executed=False, client_id=client_id).first()

    date_in = order.check_in_date
    date_out = order.check_out_date
    facilities = order.complementary_services
    room_numb = order.room_number

    room_mass = []
    item = HotelNumber.objects.all()

    for i in item:
        if (i.room_occupancy is False) and (i.room_condition is True):
            number_type: NumberType = NumberType.objects.filter(id=i.number_type_id).first()
            room_mass.append({
                'numb_id': i.id,
                'prefer_room_facilities': i.complementary_services,
                'prefer_room_numb': number_type.number_of_room
            })

    vacation = Vacation.objects.all()

    worker: Worker = Worker.objects.filter(positions_id=Positions.objects.filter(name='Уборщик').first().id)

    workers = list(worker)

    vacation_filter_for_worker = list(filter(lambda x: not vacation.filter(worker_id=x.id), workers))

    print(vacation_filter_for_worker)

    client_id = client.id

    bad_client = BlackList.objects.all()

    for i in bad_client:
        print(i.client_id, client)
        if i.client_id == client_id:
            return HttpResponseRedirect(reverse("black_list_info", args=(client_id,)))

    if request.method == 'POST':
        number = request.POST['Number']
        worker_to_number = request.POST['Worker']

        hotel_numbers: HotelNumber = HotelNumber.objects.filter(id=number).first()

        hotel_numbers.worker_id = worker_to_number
        hotel_numbers.room_occupancy = True
        order.number_id = number
        order.execution = True

        order.save()
        hotel_numbers.save()

        print(number, worker_to_number)

        return HttpResponseRedirect(reverse("select_accept_order"))

    context = {
        'f_name': f_name,
        's_name': s_name,
        't_name': t_name,
        'passport': passport,
        'date_in': date_in,
        'date_out': date_out,
        'facilities': facilities,
        'room_numb': room_numb,
        'prefer_rooms': room_mass,
        'worker': vacation_filter_for_worker
    }
    return render(request, 'client/orderACCEPT.html', context)


def restaurant_select(request):
    return render(request, 'client/restaurantSELECT.html')


def restaurant_menu_success(request):
    return render(request, 'client/restaurantMENUSuc.html')


def restaurant_menu_err(request):
    return render(request, 'client/restaurantMENUErr.html')


def restaurant_order(request):
    order_list = AdditionalOrder.objects.filter(service_id=ServiceList.objects.filter(name='Завтрак').first()) | \
                 AdditionalOrder.objects.filter(service_id=ServiceList.objects.filter(name='Обед').first()) | \
                 AdditionalOrder.objects.filter(service_id=ServiceList.objects.filter(name='Ужин').first())
    print(order_list)
    client_id = []
    number_list = []
    rest_order = []
    for item in order_list:
        client_id.append(item.client_id)
        rest_order.append(ServiceList.objects.filter(id=item.service_id).first().name)
        number_list.append(Order.objects.filter(client_id=item.client_id).first().number_id)

    context = {
        'data': zip(order_list, number_list, rest_order)
    }

    return render(request, 'client/restaurantORDER.html', context)


def restaurant_menu(request):
    menu: MenuList = MenuList.objects.all().last()
    curr_menu = menu.menu

    if request.method == 'POST':
        try:
            new_menu = request.POST['menu']
            print(new_menu)
            menu.menu = new_menu
            menu.save()
            return HttpResponseRedirect(reverse("restaurant_menu_success"))
        except Exception:
            return HttpResponseRedirect(reverse("restaurant_menu_err"))

    context = {
        'curr_menu': curr_menu,
    }
    return render(request, 'client/restaurantMENU.html', context)


def index(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        second_name = request.POST['sname']
        third_name = request.POST['tname']
        birth_date = request.POST['birth_date']
        phone_number = request.POST['phone_number']
        passport = request.POST['passport_number']
        date_in = request.POST['date_in']
        date_out = request.POST['date_out']
        room_number = request.POST['room']
        tv = request.POST.get('TV', '')
        big_bath = request.POST.get('big_bath', '')
        beauty_view = request.POST.get('beauty_view', '')
        work_space = request.POST.get('work_space', '')
        facilities = tv + big_bath + beauty_view + work_space

        order = Order()

        client: Client = Client.objects.filter(passport_field=passport).first()

        if client is None:
            client = Client()
            client.first_name = first_name
            client.second_name = second_name
            client.third_name = third_name
            client.date = birth_date
            client.passport_field = passport
            client.save()

        client_id = client.id

        bad_client = BlackList.objects.all()

        for i in bad_client:
            print(i.client_id, client)
            if i.client_id == client_id:
                return HttpResponseRedirect(reverse("black_list_info", args=(client_id,)))

        order.check_in_date = date_in
        order.check_out_date = date_out
        order.phone_number = phone_number
        order.complementary_services = facilities
        order.room_number = room_number
        order.client_id = client_id
        order.save()

        return HttpResponseRedirect(reverse("order_success"))

    return render(request, 'client/orderPAGE.html')
