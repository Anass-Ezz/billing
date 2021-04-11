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


def send_email_from_app(context):

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


def test_pdf(request, wanted_bill=None):
    template_path = 'test_pdf.html'
    if not wanted_bill:
        bill = Bill.objects.get(charged=False, user=request.user)
        context = {'bill': bill, 'data': timezone.now}
    else:
        context = {'bill': wanted_bill, 'data': timezone.now}

    send_email_from_app(context)
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


def billing(request):
    products = StockItem.objects.all()
    context = {
        'products': products
    }
    return render(request, 'main.html', context)


def detail(request, id):
    product = StockItem.objects.get(id=id)
    varient_names = VarientName.objects.filter(product=product)
    context = {
        'product': product,
        'varient_names': varient_names
    }
    return render(request, 'detail.html', context)


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


def remove_item(request, id):
    item = BillItem.objects.get(id=id)
    item.delete()
    return redirect('main:bill_summary')


def set_price(request):
    item = BillItem.objects.get(id=request.GET['id'])
    try:
        price = float(request.GET['price'])
        item.item_price = round(price, 3)
        item.save()
    except:
        pass
    return redirect('main:bill_summary')


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


def view_client(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'choose_client.html', context)


def set_client(request):
    try:
        customer = Customer.objects.get(id=request.GET['id'])
        bill = Bill.objects.get(charged=False, user=request.user)
        bill.charged_to = customer
        bill.save()
    except Customer.DoesNotExist or Customer.DoesNotExist:
        pass

    return redirect('main:bill_summary')


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
    return JsonResponse(None, safe=False)


def add_client(request):
    pass
