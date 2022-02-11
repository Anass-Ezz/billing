from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django_object_actions import DjangoObjectActions
from . import views
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


# Register your models here.

# =======for varients inline=======


class InlineVarient(NestedStackedInline):
    model = Varient
    extra = 0
    min_num = 1
    fk_name = 'varient_name'


# =======for varients inline=======

# =======for varient names inline=======
class InlineVarientName(NestedStackedInline):
    model = VarientName
    extra = 1
    min_num = 1
    max_num = 1
    fk_name = 'product'
    inlines = [InlineVarient]
# =======for varient names inline=======

# for BillItem iline


class InLineBillItem(admin.TabularInline):
    search_fields = ('id',)
    model = Bill.items.through
    extra = 0


# for BillItem iline


class BillItemAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    fields = ['quantity']
    readonly_fields = ['quantity']
    list_display = ('id', 'product', 'item_price', 'quantity')


class BillAdmin(DjangoObjectActions, admin.ModelAdmin):

    def print_bill(ModelAdmin, request, obj):
        template_path = 'test_pdf.html'

        context = {'bill': obj, 'data': timezone.now}

        views.send_email_from_app(request, context)
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

    change_actions = ('print_bill', )
    search_fields = ('id', )
    inlines = [InLineBillItem, ]


class StockItemsAdmin(NestedModelAdmin):
    search_fields = ('id', )
    fields = ["name", 'desc', "image", 'add_date', 'quantity']
    readonly_fields = ['quantity']
    inlines = [InlineVarientName]
    list_display = ("name", 'quantity')


admin.site.register(StockItem, StockItemsAdmin)
admin.site.register(VarientName)
admin.site.register(Varient)
admin.site.register(Bill, BillAdmin)
admin.site.register(BillItem, BillItemAdmin)
admin.site.register(Customer)
