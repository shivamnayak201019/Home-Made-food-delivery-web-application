from django.db import models
from datetime import datetime, timedelta
import os

# Create your models here.
class Customers1(models.Model):
    c_first_name = models.CharField(max_length=25)
    c_last_name = models.CharField(max_length=25)
    # c_speciality_f = models.ForeignKey('Speciality', models.DO_NOTHING, blank=True, null=True)
    c_phone_number = models.BigIntegerField()
    c_passward=models.CharField(max_length=200)
    c_email=models.EmailField()
    # c_avlb_op_f = models.ForeignKey('AvailableOptions', models.DO_NOTHING, blank=True, null=True)
    # subplan_f = models.ForeignKey('Subplan', models.DO_NOTHING, blank=True, null=True)

    class Meta:

        db_table = 'customers'
    
# class customerAddress(models.Model)

class spec(models.Model):
    region=models.CharField(max_length=30)
    image=models.ImageField(upload_to="media")

    class Meta:
        db_table='speciality'

# class subregion(models.Model):
#     subregionName=models.CharField(max_length=100,default='add')
#     subreg=models.ForeignKey(spec,on_delete=models.CASCADE,related_name='subregions')

#     class Meta:
#         db_table='subregion'





    # =============================chef model===================

class Chef(models.Model):
    cf_first_name=models.CharField(max_length=200)
    cf_last_name=models.CharField(max_length=200)
    cf_email=models.EmailField(max_length=200)
    cf_Phone_number=models.BigIntegerField()
    cf_passward=models.CharField(max_length=200)

    class Meta:
        db_table="Chef"

# ===============================================food upload===============================


def default_date():
    unformat=datetime.now().date() + timedelta(days=1)
    formatted_date=unformat.strftime("%d/%B/%Y")
    return formatted_date

def filepath(request,filename):
    old_filename=filename
    timeNow=datetime.now().strftime("%Y%m%d%H%M%S")
    filename="%s%s" % (timeNow,old_filename)
    return os.path.join('uploads/',filename)

class foodUpload(models.Model):
    cfid=models.ForeignKey(Chef,on_delete=models.CASCADE)
    chefspec=models.ForeignKey(spec,on_delete=models.CASCADE)
    item_name=models.CharField(max_length=200)
    item_quantity=models.IntegerField()
    item_price=models.IntegerField()
    item_date = models.CharField(max_length=200,default=default_date,blank=True)
    item_image=models.ImageField(upload_to=filepath,null=False,blank=False)
   

    class Meta:
        db_table="foodUpload"


# ================================================delivery model=============================

class Delivery(models.Model):
    d_first_name=models.CharField(max_length=200)
    d_last_name=models.CharField(max_length=200)
    d_email=models.EmailField(max_length=200)
    d_Phone_number=models.BigIntegerField()
    d_passward=models.CharField(max_length=200)

    class Meta:
        db_table="delivery"

class chefAddress(models.Model):
    chefForeign=models.ForeignKey(Chef,on_delete=models.CASCADE)
    chefLocality=models.CharField(max_length=50)
    chefState=models.CharField(max_length=50)
    chefDistrict=models.CharField(max_length=50)
    chefDivision=models.CharField(max_length=50)

class customerAddress(models.Model):
    customerForeign=models.ForeignKey(Customers1,on_delete=models.CASCADE)
    customerLocality=models.CharField(max_length=50)
    customerState=models.CharField(max_length=50)
    customerDistrict=models.CharField(max_length=50)
    customerDivision=models.CharField(max_length=50)

class cart(models.Model):
    custCartForeign=models.ForeignKey(Customers1,on_delete=models.CASCADE)
    foodUploadForeign=models.ForeignKey(foodUpload,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    amountPerQuantity=models.FloatField()
    totalAmount=models.FloatField(default=0)

    class Meta:
        db_table='cart'

class adminApproval(models.Model):
    foodUploadChef=models.ForeignKey(foodUpload,on_delete=models.CASCADE)
    approval=models.BooleanField('Approve',default=False)

class order(models.Model):
    ordernumber=models.CharField(max_length=100)
    orderdate=models.DateField(max_length=100)
    custdetail=models.ForeignKey(Customers1,on_delete=(models.CASCADE))
    custaddr=models.ForeignKey(customerAddress,on_delete=models.CASCADE)
    orderstatus=models.CharField(max_length=100)

    class Meta:
        db_table="order"

class payment(models.Model):
    customerid=models.ForeignKey(Customers1,on_delete=models.CASCADE)
    oid=models.ForeignKey(order,on_delete=models.CASCADE)
    paymentstatus=models.CharField(max_length=100,default='pending')
    transactionid=models.CharField(max_length=200)
    paymentmode=models.CharField(max_length=100,default='paypal')

    class Meta:
        db_table='payment'

class orderdetail(models.Model):
    ordernumber=models.CharField(max_length=100)
    customerid=models.ForeignKey(Customers1,on_delete=models.CASCADE)
    cartid=models.ForeignKey(foodUpload,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalprice=models.IntegerField()
    paymentid=models.ForeignKey(payment,on_delete=models.CASCADE,null=True)
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now=True)

    class Meta:
        db_table='orderdetail'



   

