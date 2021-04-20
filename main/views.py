from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
from django.forms.models import model_to_dict
from django.core import serializers
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json


@login_required(login_url='/login')
def send_email_from_app(request, context):

    subject = 'FACTURE LIVEX'
    # bill = Bill.objects.get(charged=False, user=request.user)
    # context = {'bill': bill, 'data': timezone.now}
    html_message = render_to_string(
        'test_mail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.APPLICATION_EMAIL
    to = [
        'anassbelkadi66@gmail.com',
        # 'syoussefama@gmail.com',
        # 'anas.belkadi@um6p.ma'
    ]

    mail.send_mail(subject, plain_message, from_email,
                   to, html_message=html_message)


@login_required(login_url='/login')
def test_pdf(request, wanted_bill=None):
    template_path = 'test_pdf.html'
    if not wanted_bill:
        bill = Bill.objects.get(charged=False, user=request.user)
        context = {'bill': bill, 'data': timezone.now}
    else:
        context = {'bill': wanted_bill, 'data': timezone.now}

    send_email_from_app(request, context)
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required(login_url='/login')
def billing(request):
    if request.method == 'POST':
        products = StockItem.objects.filter(
            Q(name__startswith=request.POST['kw']) | Q(name__icontains=request.POST['kw']))
        if not products.exists():
            products = []
            varients = Varient.objects.filter(
                Q(name__startswith=request.POST['kw']) | Q(name__icontains=request.POST['kw']))
            for varient in varients:
                product = varient.varient_name.product
                print(product)
                if not product in products:
                    products.append(product)

    else:
        products = StockItem.objects.all()
    context = {
        'products': products
    }
    return render(request, 'main.html', context)


@login_required(login_url='/login')
def detail(request, id):
    product = StockItem.objects.get(id=id)
    varient_names = VarientName.objects.filter(product=product)
    context = {
        'product': product,
        'varient_names': varient_names
    }
    return render(request, 'detail.html', context)


@login_required(login_url='/login')
def add_item(request):
    print(request.POST)
    bill, created = Bill.objects.get_or_create(
        user=request.user, charged=False)
    item = StockItem.objects.get(id=request.POST['product_id'])
    bill_item = BillItem.objects.create(product=item, user=request.user)
    bill.items.add(bill_item)
    for key in request.POST:
        if 'varient' in key:
            varient = Varient.objects.get(id=request.POST[key])
            bill_item.choosed_varients.add(varient)
            bill_item.save()
    bill.save()

    # Bill.objects.get(charged=False).save()
    return redirect('main:detail', item.id)


@login_required(login_url='/login')
def bill_summary(request):
    try:
        bill = Bill.objects.get(user=request.user, charged=False)
        bill.save()

        context = {
            'bill': bill
        }
    except Bill.DoesNotExist:
        context = {}

    return render(request, 'bill_summary copy.html', context)


@login_required(login_url='/login')
def remove_item(request, id):
    item = BillItem.objects.get(id=id)
    item.delete()
    return redirect('main:bill_summary')


@login_required(login_url='/login')
def set_price(request):
    item = BillItem.objects.get(id=request.GET['id'])
    try:
        price = float(request.GET['price'])
        item.item_price = round(price, 3)
        item.save()
    except:
        pass
    return redirect('main:bill_summary')


@login_required(login_url='/login')
def check_quantity(item, quantity):

    if item.choosed_varients.all():

        for var in item.choosed_varients.all():
            varient = Varient.objects.get(id=var.id)
            if varient.quantity > item.quantity:
                return True
            else:
                return False
                item.quantity = varient.quantity
                item.save()
                break
    else:
        return True


@login_required(login_url='/login')
def set_quantity(request):
    try:
        check = None
        quantity = int(request.GET['quantity'])
        print(quantity)
        item = BillItem.objects.get(id=request.GET['id'])
        print(item)
        for var in item.choosed_varients.all():
            if var.quantity >= quantity:
                check = True
            else:
                check = False
                break
        if check:
            item.quantity = quantity
            item.save()
            return redirect('main:bill_summary')
        else:
            item.save()
            return redirect('main:bill_summary')

    except:
        return redirect('main:bill_summary')


@login_required(login_url='/login')
def set_discount(request):
    try:
        bill = Bill.objects.get(charged=False, user=request.user)
        discount = float(request.GET['discount'])
        if discount < bill.bill_total:
            bill.discount = discount
            bill.save()
    except:
        pass

    return redirect('main:bill_summary')


@login_required(login_url='/login')
def finish_order(request):
    bill = Bill.objects.get(charged=False, user=request.user)
    for item in bill.items.all():
        print(item.product.quantity)
        product = StockItem.objects.get(id=item.product.id)
        check = check_quantity(item, product)

        if check:
            for var in item.choosed_varients.all():
                varient = Varient.objects.get(id=var.id)
                varient.quantity -= item.quantity
                varient.save()
            product.quantity -= item.quantity
            product.save()
        else:
            pass
    # return redirect()


@login_required(login_url='/login')
def view_client(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'choose_client.html', context)


@login_required(login_url='/login')
def set_client(request):
    try:
        customer = Customer.objects.get(id=request.GET['id'])
        bill, created = Bill.objects.get_or_create(
            charged=False, user=request.user)
        bill.charged_to = customer
        bill.save()
    except Customer.DoesNotExist or Bill.DoesNotExist:
        pass

    return redirect('main:bill_summary')


@login_required(login_url='/login')
def search_client(request):
    if request.is_ajax():
        if request.GET['kw']:
            try:
                customers = Customer.objects.filter(id=request.GET['kw'])
            except:
                customers = Customer.objects.filter(
                    Q(first_name__startswith=request.GET['kw']) |
                    Q(last_name__startswith=request.GET['kw'])
                )

            if customers:
                return JsonResponse(serializers.serialize('json', customers), safe=False)
        else:
            customers = Customer.objects.all()
            return JsonResponse(serializers.serialize('json', customers), safe=False)

    return JsonResponse(None, safe=False)


@login_required(login_url='/login')
def add_client(request):
    if request.method == 'POST':
        if request.POST['first_name'] and request.POST['last_name'] and request.POST['city'] and \
                request.POST['email'] and request.POST['phone']:
            customer = Customer.objects.create(first_name=request.POST['first_name'],
                                               last_name=request.POST['last_name'],
                                               city=request.POST['city'],
                                               email=request.POST['email'],
                                               phone=request.POST['phone'])
            if request.POST['address']:
                customer.address = request.POST['address']
                customer.save()
    return redirect('main:view_client')


def login_view(request):
    # print('yeah')
    if request.user.is_authenticated:
        return redirect('main:billing')
    else:
        if request.method == 'POST':
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user:
                login(request, user)
                return redirect('main:billing')
            else:
                return render(request, 'login_page.html')
        else:
            return render(request, 'login_page.html')
