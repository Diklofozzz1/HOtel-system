from io import BytesIO

from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.views import View
from xhtml2pdf import pisa

from hotel_numbers.models import HotelNumber, NumberType, Storage, WashHouse, Provider, StaffOrder
from reg.models import Worker, Positions, Vacation
from .models import Client, Order, BlackList, ServiceList, AdditionalOrder, MenuList

User = get_user_model()


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("select")


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encodings='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


data = {}


class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('client/pdf_template.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response


@login_required(login_url='/auth/')
def search_err(request):
    return render(request, 'client/orderSEARCHErr.html')


@login_required(login_url='/auth/')
def client_select(request):
    return render(request, 'client/selectORDER_ACCEPT.html')


@login_required(login_url='/auth/')
def order_success(request):
    return render(request, 'client/orderSUCCESS.html')


@login_required(login_url='/auth/')
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


@login_required(login_url='/auth/')
def client_out_search_err(request):
    return render(request, 'client/clientOUTSERCErr.html')


@login_required(login_url='/auth/')
def client_out_suc(request):
    return render(request, 'client/clientOUTSERCHSuc.html')


@login_required(login_url='/auth/')
def client_out_err(request):
    return render(request, 'client/clientOUTErr.html')


@login_required(login_url='/auth/')
def client_out(request, client_id):
    try:
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
    except Exception:
        return HttpResponseRedirect(reverse("client_out_search_err"))

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


@login_required(login_url='/auth/')
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


@login_required(login_url='/auth/')
def black_list_err(request, client):
    if request.method == 'POST':
        client_id = client
        return HttpResponseRedirect(reverse("black_list_add", args=(client_id,)))
    return render(request, 'client/blacklistERR.html')


@login_required(login_url='/auth/')
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


@login_required(login_url='/auth/')
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


@login_required(login_url='/auth/')
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


@login_required(login_url='/auth/')
def additional_order(request, client_id):
    client: Client = Client.objects.filter(id=client_id).first()

    f_name = client.first_name
    s_name = client.second_name
    t_name = client.third_name

    vacation = Vacation.objects.all()

    service_list = ServiceList.objects.all()

    worker: Worker = Worker.objects.filter(positions_id=Positions.objects.filter(name='??????????????????').first().id)

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


@login_required(login_url='/auth/')
def additional_search_err(request):
    return render(request, 'client/additional_SEARCHErr.html')


@login_required(login_url='/auth/')
def additional_order_success(request, client_id):
    context = {
        'client_id': client_id
    }
    return render(request, 'client/additional_SUCCESS.html', context)


@login_required(login_url='/auth/')
def additional_err(request):
    return render(request, 'client/additional_err.html')


@login_required(login_url='/auth/')
def cleaning_room_err(request):
    return render(request, 'client/numberCLININGErr.html')


@login_required(login_url='/auth/')
def storage(request):
    storage_fill = Storage.objects.all()
    linel: Storage = Storage.objects.filter(id=1).first()
    dirty_staff = linel.dirty_staff

    context = {
        'storage': storage_fill,
        'dirty_staff': dirty_staff
    }
    return render(request, 'client/sorage.HTML', context)


@login_required(login_url='/auth/')
def storage_order_suc(request):
    return render(request, 'client/stuffORDER_storage_suc.html')


@login_required(login_url='/auth/')
def storage_order_err(request):
    return render(request, 'client/stuffORDER_storage_err.html')


@login_required(login_url='/auth/')
def storage_order(request):
    storage_fill = Storage.objects.all()
    linel: Storage = Storage.objects.filter(id=1).first()
    dirty_staff = linel.dirty_staff
    provider = Provider.objects.all()
    provider_list = [i.name for i in provider]

    vacation = Vacation.objects.all()

    worker: Worker = Worker.objects.filter(positions_id=Positions.objects.filter(name='??????????????????????????').first().id)

    workers = list(worker)

    vacation_filter_for_worker = list(filter(lambda x: not vacation.filter(worker_id=x.id), workers))

    if request.method == "POST":
        try:
            linel_to_order = request.POST['Linel']
            shampoo = request.POST['Shampoo']
            wash_gel = request.POST['WashGel']
            brush = request.POST['Brush']
            razor = request.POST['Razor']
            paste = request.POST['Paste']
            paper = request.POST['Paper']
            soap = request.POST['Soap']
            order_date = request.POST['order_date']
            order_provider = request.POST['Provider']

            storage_linel: Storage = Storage.objects.filter(name='???????????????? ??????????').first()
            storage_shampoo: Storage = Storage.objects.filter(name='??????????????').first()
            storage_wash_gel: Storage = Storage.objects.filter(name='???????? ?????? ????????').first()
            storage_brush: Storage = Storage.objects.filter(name='??????????').first()
            storage_razor: Storage = Storage.objects.filter(name='????????????').first()
            storage_paste: Storage = Storage.objects.filter(name='??????????').first()
            storage_paper: Storage = Storage.objects.filter(name='?????????????????? ????????????').first()
            storage_soap: Storage = Storage.objects.filter(name='????????').first()

            count = int(linel_to_order) + int(shampoo) + int(wash_gel) + int(brush) + int(razor) + int(paste) + int(
                paper) + int(soap)
            coast = storage_linel.coast * float(linel_to_order) + storage_shampoo.coast * float(
                shampoo) + storage_wash_gel.coast * float(wash_gel) + storage_brush.coast * float(
                brush) + storage_razor.coast * float(razor) + storage_paste.coast * float(
                paste) + storage_paper.coast * float(paper) + storage_soap.coast * float(soap)

            order_staff = StaffOrder()

            order_staff.name = '??????????'
            order_staff.coast = coast
            order_staff.order_date = order_date
            order_staff.count = count
            order_staff.provider_id = provider.filter(name=order_provider).first().id
            order_staff.worker_id = request.POST['Worker']
            order_staff.save()

            storage_linel.quantity = storage_linel.quantity + int(linel_to_order)
            storage_linel.save()

            storage_shampoo.quantity = storage_shampoo.quantity + int(shampoo)
            storage_shampoo.save()

            storage_wash_gel.quantity = storage_wash_gel.quantity + int(wash_gel)
            storage_wash_gel.save()

            storage_brush.quantity = storage_brush.quantity + int(brush)
            storage_brush.save()

            storage_razor.quantity = storage_razor.quantity + int(razor)
            storage_razor.save()

            storage_paste.quantity = storage_paste.quantity + int(paste)
            storage_paste.save()

            storage_paper.quantity = storage_paper.quantity + int(paper)
            storage_paper.save()

            storage_soap.quantity = storage_soap.quantity + int(soap)
            storage_soap.save()

            return HttpResponseRedirect(reverse("storage_order_suc"))
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse("storage_order_err"))

    context = {
        'storage': storage_fill,
        'dirty_staff': dirty_staff,
        'provider_list': provider_list,
        'worker': vacation_filter_for_worker
    }
    return render(request, 'client/stuffORDER_storage.html', context)


@login_required(login_url='/auth/')
def order_stuff_washhouse_select(request):
    return render(request, 'client/stuffORDER_WASHHOUSE_select.html')


@login_required(login_url='/auth/')
def order_stuff_washhouse(request):
    linel: Storage = Storage.objects.filter(id=1).first()
    dirty_staff = linel.dirty_staff

    if request.method == 'POST':
        try:
            count_to_wash = int(request.POST['count_to_wash'])
            order_to_wash = WashHouse()

            if int(count_to_wash) <= int(dirty_staff):
                order_to_wash.number = count_to_wash
                order_to_wash.coast = count_to_wash * 100
                order_to_wash.article = Storage.objects.filter(id=1).first()
                order_to_wash.save()

                linel.dirty_staff = linel.dirty_staff - count_to_wash
                linel.save()
                return HttpResponseRedirect(reverse("order_stuff_washhouse_suc"))
            else:
                return HttpResponseRedirect(reverse("order_stuff_washhouse_err"))

        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse("order_stuff_washhouse_err"))

    context = {
        'dirty_staff': dirty_staff
    }
    return render(request, 'client/stuffORDER_WASHHOUSE.html', context)


@login_required(login_url='/auth/')
def order_stuff_washhouse_err(request):
    return render(request, 'client/stuffORDER_WASHHOUSE_Err.html')


@login_required(login_url='/auth/')
def order_stuff_washhouse_suc(request):
    return render(request, 'client/stuffORDER_WASHHOUSE_Suc.html')


@login_required(login_url='/auth/')
def washhouse_compliting(request):
    order_mass = []
    item = WashHouse.objects.all()

    for i in item:
        if i.condition is False:
            order_mass.append({
                'order_id': i.id,
                'number': i.number,
                'coast': i.coast,
            })

    if request.method == "POST":
        try:
            order_number = request.POST['Number']
            order: WashHouse = WashHouse.objects.filter(id=order_number).first()
            order.condition = True
            order.save()

            linel: Storage = Storage.objects.filter(id=1).first()
            linel.quantity = linel.quantity + order.number
            linel.save()

            return HttpResponseRedirect(reverse("washhouse_compliting"))
        except Exception:
            return HttpResponseRedirect(reverse("order_stuff_washhouse_err"))

    context = {
        'orders': order_mass
    }

    return render(request, 'client/stuffORDER_WASHHOUSE_compliting.html', context)


@login_required(login_url='/auth/')
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

            count_of_resident = number.number_of_residents

            storage = Storage.objects.all()

            linel: Storage = Storage.objects.filter(id=1).first()
            linel.dirty_staff = linel.dirty_staff + count_of_resident
            linel.save()

            for item in storage:
                if item.quantity > count_of_resident:
                    item.quantity = item.quantity - count_of_resident
                    item.save()
                else:
                    return HttpResponseRedirect(reverse("cleaning_room_err"))

            return HttpResponseRedirect(reverse("cleaning_room"))
        except Exception:
            return HttpResponseRedirect(reverse("cleaning_room_err"))

    context = {
        'hotel_numbers': room_mass,
    }

    return render(request, 'client/numberCLINING.html', context)


@login_required(login_url='/auth/')
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


@login_required(login_url='/auth/')
def order_accept(request, client_id):
    try:
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

        worker: Worker = Worker.objects.filter(positions_id=Positions.objects.filter(name='??????????????').first().id)

        workers = list(worker)

        vacation_filter_for_worker = list(filter(lambda x: not vacation.filter(worker_id=x.id), workers))

        print(vacation_filter_for_worker)

        client_id = client.id

        bad_client = BlackList.objects.all()

        for i in bad_client:
            print(i.client_id, client)
            if i.client_id == client_id:
                return HttpResponseRedirect(reverse("black_list_info", args=(client_id,)))
    except Exception:
        return HttpResponseRedirect(reverse("search_err"))

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


@login_required(login_url='/auth/')
def restaurant_select(request):
    return render(request, 'client/restaurantSELECT.html')


@login_required(login_url='/auth/')
def restaurant_menu_success(request):
    return render(request, 'client/restaurantMENUSuc.html')


@login_required(login_url='/auth/')
def restaurant_menu_err(request):
    return render(request, 'client/restaurantMENUErr.html')


@login_required(login_url='/auth/')
def restaurant_order(request):
    order_list = AdditionalOrder.objects.filter(service_id=ServiceList.objects.filter(name='??????????????').first()) | \
                 AdditionalOrder.objects.filter(service_id=ServiceList.objects.filter(name='????????').first()) | \
                 AdditionalOrder.objects.filter(service_id=ServiceList.objects.filter(name='????????').first())
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


@login_required(login_url='/auth/')
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


@login_required(login_url='/auth/')
def order_stuff(request):
    return render(request, 'client/stuffORDER.html')


@login_required(login_url='/auth/')
def profit(request):
    completed_order = Order.objects.filter(executed=True)
    additional_order = AdditionalOrder.objects.all()

    number_profit: float = 0.

    for item in completed_order:
        number_profit += float(HotelNumber.objects.filter(id=item.number_id).first().coast_per_day) * float(
            ((item.check_out_date - item.check_in_date).days))

    aditional_profit: float = 0.

    for item in additional_order:
        aditional_profit += item.coast

    all_profit = aditional_profit + number_profit

    washhose_order = WashHouse.objects.filter(condition=True)

    wash_coast: float = 0.

    for item in washhose_order:
        wash_coast += item.coast

    stuff_order = StaffOrder.objects.all()
    stuff_coast: float = 0.

    for item in stuff_order:
        stuff_coast += item.coast

    worker = Worker.objects.all()
    worker_coast: float = 0.

    for item in worker:
        worker_coast += float(Positions.objects.filter(id=item.positions_id).first().payment)

    all_coast = worker_coast + stuff_coast + wash_coast

    sum_profit = all_profit - all_coast

    context = {
        'number_profit': number_profit,
        'aditional_profit': aditional_profit,
        'all_profit': all_profit,
        'wash_coast': wash_coast,
        'stuff_coast': stuff_coast,
        'worker_coast': worker_coast,
        'all_coast': all_coast,
        'sum_profit': sum_profit
    }

    global data
    data = context

    return render(request, 'client/profit.html', context)


@login_required(login_url='/auth/')
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
