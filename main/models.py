from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
import random


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    frequancy = models.IntegerField(default=0)

    def __str__(self):
        return (self.first_name+' '+self.last_name)


class StockItem(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=1000)
    stock_price = models.FloatField(null=True, blank=True)
    image = models.ImageField(
        upload_to='images', default='images/default.png', null=True, blank=True)
    add_date = models.DateTimeField(default=timezone.now)

    def quantity(self):
        total_quantity = 0
        varient_names = self.varientname_set.all()
        for varient_name in varient_names:
            varints = varient_name.varient_set.all()
            for varient in varints:
                total_quantity += varient.quantity
        return(total_quantity)

    def __str__(self):
        return self.name


class Varient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0, blank=True)
    varient_name = models.ForeignKey(
        'VarientName', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name+" ( ID: "+str(self.id)+")"


class VarientName(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(StockItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BillItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    item_price = models.FloatField(default=0, null=True, blank=True)
    item_total = models.FloatField(null=True, blank=True)
    choosed_varients = models.ManyToManyField(Varient, blank=True)
    add_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        try:
            bill = Bill.objects.get(charged=False)
            total = round(self.quantity*self.item_price, 3)
            self.item_total = total
            super(BillItem, self).save(*args, **kwargs)
            bill.save()
        except:
            pass

    def __str__(self):
        return self.product.name


class Bill (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(BillItem, blank=True)
    charged = models.BooleanField(default=False)
    bill_total = models.FloatField(default=0, null=True)
    charged_to = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)
    add_date = models.DateTimeField(
        auto_now_add=timezone.now, blank=True, null=True)
    discount = models.FloatField(default=0, null=True, blank=True)
    after_discount = models.FloatField(null=True)

    def __str__(self):
        if self.charged_to:
            return (self.charged_to.first_name + ' ' + self.charged_to.last_name)
        else:
            return("BILL "+str(self.add_date.date()))

    def save(self, *args, **kwargs):
        total = 0
        # --------------------FOR TOTAL-------------------
        # if self.items.exists():
        try:
            for item in self.items.all():
                print('yeah bill')
                total += item.item_total
            self.bill_total = round(total, 3)
            print(total)
        except:
            pass

        # --------------------FOR TOTAL-------------------
        # --------------------FOR DISCOUNT-------------------
        if self.discount:
            self.after_discount = round(
                self.bill_total - self.bill_total*(self.discount/100), 3)
        else:
            self.discount = 0
            self.after_discount = round(self.bill_total, 3)
        # --------------------FOR DISCOUNT-------------------

        super(Bill, self).save(*args, **kwargs)
