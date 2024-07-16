from django.shortcuts import render,redirect
from django.views.generic import ListView
from .models import Customers1,spec,foodUpload,Chef,chefAddress,customerAddress,cart,adminApproval,order,payment,orderdetail
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Q
from django.contrib import messages
from datetime import date
import razorpay
from django.conf import settings




# Create your views here.

def register(request):
    if request.method=="GET":
        return render(request,"HM_Register.html")
    elif request.method=="POST":
        firstname=request.POST.get('fn')
        lastname=request.POST.get('ln')
        email=request.POST.get('em')
        pwd=request.POST.get('pass')
        epwd=make_password(pwd)
        phoneno=request.POST.get('pn')
        if request.POST.get('options')=='user':
            customerObj=Customers1(c_first_name=firstname,c_last_name=lastname,c_phone_number=phoneno,c_passward=epwd,c_email=email)
            customerObj.save()
            return redirect('../login')
        elif request.POST.get('options')=='chef':
            chefobj=Chef(cf_first_name=firstname,cf_last_name=lastname,cf_Phone_number=phoneno,cf_passward=epwd,cf_email=email)
            chefobj.save()
            return redirect('../login')

        
# def chefregister(request):
#     if request.method=="GET":
#         return render(request,"chef_register.html")
#     elif request.method=="POST":
#         cffn=request.POST.get('fn')
#         cfln=request.POST.get('ln')
#         cfemail=request.POST.get('em')
#         cfpass=request.POST.get('pass')
#         cfepass=make_password(cfpass)
#         cfpn=request.POST.get('pn')
#         chefobj=Chef(cf_first_name=cffn,cf_last_name=cfln,cf_email=cfemail,cf_Phone_number=cfpn,cf_passward=cfepass)
#         chefobj.save()
#         return redirect('../cheflogin')
def login(request):
    if request.method=="GET":
        return render(request,'HM_LOGIN.html')
    elif request.method=="POST":
        lem=request.POST.get('lemail')
        lpass=request.POST.get('lpwd')
        lobj=Customers1.objects.filter(c_email=lem)
        lcfobj=Chef.objects.filter(cf_email=lem)
        if lobj:
            lobj1=Customers1.objects.get(c_email=lem)
            flag=check_password(lpass,lobj1.c_passward)
            if flag:
                request.session['sessionval']=lobj1.c_email
                request.session['sessionname']=lobj1.c_first_name
                
             
                return redirect('../location')
            else:
                return render(request,'HM_login.html',{'msg':'incorrect email or password'})
        elif lcfobj:
            lobj1=Chef.objects.get(cf_email=lem)
            flag=check_password(lpass,lobj1.cf_passward)
            if flag:
                request.session['sessionval']=lobj1.cf_email
                request.session['sessionname']=lobj1.cf_first_name
             
                return redirect('../location')
            else:
                return render(request,'HM_login.html',{'msg':'incorrect email or password'})
        else:
            return render(request,'HM_login.html',{'msg':'incorrect email or password'})
        




class homeMade(ListView):
    model=spec
    template_name='home_made.html'
    context_object_name='foodobj'

    def get_context_data(self,**kwargs):
        try:
            data=self.request.session['sessionname']
            context=super().get_context_data(**kwargs)
            context['session']=data
            return context
        except:
            context=super().get_context_data(**kwargs)
            return context

def search(request):
    if request.method=="POST":
        session=request.session['sessionname']
        searchdata=request.POST.get('searchquery')
        foodobj=spec.objects.filter(Q(region__icontains=searchdata))
        return render(request,'home_made.html',{'foodobj':foodobj,'session':session})
    
def join(request):
    if request.method=="GET":
        return render(request,"join.html")

def delivery(request):
    if request.method=="GET":
        return redirect('../delivery')

def service(request):
    if request.method=="GET":
        return redirect('../service')
    
def foodItem(request):
    if request.method=="GET":
        cfem=request.session['sessionval']
        session=request.session['sessionname']
        cfname=request.session['sessionname']
        cfobj1=Chef.objects.get(cf_email=cfem)
        foodupobj=foodUpload.objects.filter(cfid=cfobj1.id)
        chefAddressObj=chefAddress.objects.get(chefForeign=cfobj1.id)
        cuisineObj=spec.objects.all()
        approved_food = adminApproval.objects.filter(foodUploadChef__in=foodupobj, approval=True).values_list('foodUploadChef', flat=True)
        approved_food_items = foodUpload.objects.filter(id__in=approved_food)
       
        return render(request,"foodItem.html",{'sessionname':cfname,'foodupobj':approved_food_items,'chefAddressObj':chefAddressObj,'cuisineObj':cuisineObj,'session':session})
    
    elif request.method=='POST':
        cfem=request.session['sessionval']  
        cfname=request.session['sessionname']
        session=request.session['sessionname']
        cfobj1=Chef.objects.get(cf_email=cfem)
        ufspec=request.POST.get('ufspec')
        specobj=spec.objects.get(region=ufspec)
        ufname=request.POST.get('ufname')
        ufkg=request.POST.get('ufkg')
        ufprice=request.POST.get('ufprice')
        ufimg=request.FILES['ufimg']
        foodupobj=foodUpload(cfid=cfobj1,chefspec=specobj,item_name=ufname,item_quantity=ufkg,item_price=ufprice,item_image=ufimg)
        foodupobj.save()
        print(specobj.region)
        if(specobj.region=="others"):
            print(specobj.region)
            print(type(specobj.region))
            adminobj=adminApproval(foodUploadChef=foodupobj)
            adminobj.save()
            messages.info(request,'your item has been submited for approval')
        else:
            adminobj=adminApproval(foodUploadChef=foodupobj,approval=True)
            adminobj.save()
           
        foodupobj=foodUpload.objects.filter(cfid=cfobj1.id)
        approved_food=adminApproval.objects.filter(foodUploadChef__in=foodupobj,approval=True).values_list('foodUploadChef',flat=True)
        approved_food_items=foodUpload.objects.filter(id__in=approved_food)
        cuisineObj=spec.objects.all()
        
        return render(request,'foodItem.html',{'sessionname':cfname,'foodupobj':approved_food_items,'cuisineObj':cuisineObj,'adminobj':adminobj,'session':session})


    
def location(request):
    if request.method=="GET":
        sessobj=request.session['sessionval']
        session=request.session['sessionname']
        chefobj=Chef.objects.filter(cf_email=sessobj)
        if chefobj:
            getchefobj=Chef.objects.get(cf_email=sessobj)
            chefAddressObj=chefAddress.objects.filter(chefForeign=getchefobj.id)
            if chefAddressObj:
                return redirect('../homeMade')
            else:
                return render(request,"location.html",{'session':session})


        custobj=Customers1.objects.filter(c_email=sessobj)
        
        if custobj:
            getcust=Customers1.objects.get(c_email=sessobj)
            custcart=cart.objects.filter(custCartForeign=getcust)
            print(getcust.c_email)
            if custcart:
                getcustloc=customerAddress.objects.filter(customerForeign=getcust)
                if getcustloc:
                     custAddrObj=customerAddress.objects.get(customerForeign=getcust.id)
                     print(custAddrObj.customerDistrict)
                     return redirect('../showloc')
                else:
                    return render(request,"location.html",{'getcust':getcust,'session':session})

            return redirect('../homeMade')
            
    elif request.method=="POST":
        sessobj=request.session['sessionval']
        checkObjChef=Chef.objects.filter(cf_email=sessobj)
        checkObjCust=Customers1.objects.filter(c_email=sessobj)
        local=request.POST.get('locality')
        state1=request.POST.get('state')
        district1=request.POST.get('district')
        division1=request.POST.get('city')
        if checkObjChef:
            chefobj=Chef.objects.get(cf_email=sessobj)
            chefAddressObj=chefAddress(chefForeign=chefobj,chefLocality=local,chefState=state1,chefDistrict=district1,chefDivision=division1)
            chefAddressObj.save()
            # chefAddressObj=chefAddress.objects.filter(chefForeign=chefobj.id)
            return redirect('../foodItem')
          

        elif checkObjCust:
            customerobj=Customers1.objects.get(c_email=sessobj)
            customerAddressObj=customerAddress(customerForeign=customerobj,customerLocality=local,customerState=state1,customerDistrict=district1,customerDivision=division1)
            customerAddressObj.save()
            return redirect('../showloc')
        
def chefloc(request,pk):
    if request.method=="GET":
         session=request.session['sessionname']
         print(pk)
         chefdistinct=foodUpload.objects.filter(chefspec=pk)
         chef_ids = chefdistinct.values_list('cfid', flat=True).distinct()     ##note
                                                #  The values() method returns a QuerySet containing dictionaries:
                                                # <QuerySet [{'comment_id': 1}, {'comment_id': 2}]>
                                                # The values_list() method returns a QuerySet containing tuples:
                                                # <QuerySet [(1,), (2,)]>    
                                                # f you are using values_list() with a single field, you can use flat=True to return a QuerySet of single values instead of 1-tuples:
                                                # <QuerySet [1, 2]>      
                                                #  ##note
                                                #  sendSpec=chefdistinct.values_list('chefspec').distinct()                                              
         
         chefSpecObj = chefAddress.objects.filter(chefForeign__in=chef_ids) 
        #  chefAddrObj=chefAddress.objects.filter(chefForeign=chefSpecObj)
                               
         sendSpec=pk
         print(sendSpec)
         return render(request,'chefLocation.html',{'chefSpecObj':chefSpecObj,'sendSpec':sendSpec,'session':session})
      
        
def dailyMenu(request,pk):
    if request.method=="GET":
        sendSpec=request.GET.get('sendSpec')
        session=request.session['sessionname']
        print(sendSpec)
        print(type(sendSpec))
        specobj=spec.objects.get(id=sendSpec)
        chefAddrObj=chefAddress.objects.get(chefForeign=pk)
        chefobj=Chef.objects.get(id=pk)
        chefFood=foodUpload.objects.filter(cfid=chefobj,chefspec=specobj)
        approved_food=adminApproval.objects.filter(foodUploadChef__in=chefFood,approval=True).values_list('foodUploadChef',flat=True)
        approved_food_items=foodUpload.objects.filter(id__in=approved_food)
        sendChefId=pk
        return render(request,"daily_menu.html",{'chefFood':approved_food_items,'chefAddrObj':chefAddrObj,'sendSpec':sendSpec,'sendChefId':sendChefId,'session':session})
        # chefSpecObj=Chef.objects.filter()

def addToCart(request):
    if request.method=="GET":
        sendChefId=request.GET.get('sendChefId')
        session=request.sesssion['sessionname']
        sendSpec=request.GET.get('sendSpec')
        specobj=spec.objects.get(id=sendSpec)
        chefAddrObj=chefAddress.objects.get(chefForeign=sendChefId)
        chefobj=Chef.objects.get(id=sendSpec)
        chefFood=foodUpload.objects.filter(cfid=chefobj,chefspec=specobj)
        return render(request,"daily_menu.html",{'chefFood':chefFood,'chefAddrObj':chefAddrObj,'sendSpec':sendSpec,'sendChefId':sendChefId,'session':session})
        
    elif request.method=="POST":
        custsession=request.session['sessionval']
        getCustomer=Customers1.objects.filter(c_email=custsession)
        if getCustomer:
            session=request.session['sessionname']
            sendChefId=request.GET.get('sendChefId')
            sendSpec=request.GET.get('sendSpec')
            specobj=spec.objects.get(id=sendSpec)
            chefAddrObj=chefAddress.objects.get(chefForeign=sendChefId)
            chefobj=Chef.objects.get(id=sendChefId)
            chefFood=foodUpload.objects.filter(cfid=chefobj,chefspec=specobj)



            foodId=request.POST.get('add')
            getFoodSelected=foodUpload.objects.get(id=foodId)
            getCustomer=Customers1.objects.get(c_email=custsession)
            previousAddedItem=cart.objects.filter(custCartForeign=getCustomer.id,foodUploadForeign=getFoodSelected)
            if previousAddedItem:
                cartobj=cart.objects.get(custCartForeign=getCustomer.id,foodUploadForeign=getFoodSelected)
                cartobj.quantity+=1
                cartobj.totalAmount=cartobj.quantity*cartobj.amountPerQuantity
                cartobj.save()
            else:
                cartobj=cart(custCartForeign=getCustomer,foodUploadForeign=getFoodSelected,quantity=1,amountPerQuantity=getFoodSelected.item_price*1,totalAmount=getFoodSelected.item_price*1)
                cartobj.save()
            return render(request,'daily_menu.html',{'chefFood':chefFood,'chefAddrObj':chefAddrObj,'sendSpec':sendSpec,'sendChefId':sendChefId,'session':session})
        else:
            messages.info(request,"kindly register as customer")
            return redirect('../register/')
    
def viewcart(request):
    custsession=request.session['sessionval']
    session=request.session['sessionname']
    getCustomer=Customers1.objects.get(c_email=custsession)
    cartobj=cart.objects.filter(custCartForeign=getCustomer.id)
    return render(request,'cart.html',{'cartobj':cartobj,'session':session})
    
def changequantity(request):
    if request.method=="POST":
        getItemId=request.POST.get('itemId')
        print(getItemId)
        custsession=request.session['sessionval']
        getCustomer=Customers1.objects.get(c_email=custsession)
        print(getCustomer)
        # getItem=cart.objects.get(foodUploadForeign=getItemId)
        # print(getItem.id)
        getCartObj=cart.objects.get(custCartForeign=getCustomer.id,foodUploadForeign=getItemId)
        getChangeQuantity=request.POST.get('cqbtn')
        if getChangeQuantity=='-':
       
            if getCartObj.quantity>1:
                getCartObj.quantity-=1
                getCartObj.totalAmount=getCartObj.quantity*getCartObj.amountPerQuantity
                getCartObj.save()
            elif getCartObj.quantity==1:
                getCartObj.delete()
        elif getChangeQuantity=='+':
             getCartObj.quantity+=1
             getCartObj.totalAmount=getCartObj.quantity*getCartObj.amountPerQuantity
             getCartObj.save()
        return redirect('../viewcart')

def summary(request):
    custsession=request.session['sessionval']
    session=request.session['sessionname']
    custobj=Customers1.objects.get(c_email=custsession)
    cartSummary=cart.objects.filter(custCartForeign=custobj.id)
    totalbill=0
    for i in cartSummary:
        totalbill+=i.totalAmount
    return render(request,'summary.html',{'session':custsession,'cartSummary':cartSummary,'totalbill':totalbill,'session':session})

def showloc(request):
    custsession=request.session['sessionval']
    custobj=Customers1.objects.get(c_email=custsession)
    custAddrObj=customerAddress.objects.get(customerForeign=custobj.id)
    print(custAddrObj.customerDistrict)
    datetimev=date.today()
    orderobj=order(custdetail=custobj,custaddr=custAddrObj,orderdate=datetimev,orderstatus="pending")
    orderobj.save()

    ono=str(orderobj.id)+str(datetimev).replace('-','')
    orderobj.ordernumber=ono
    orderobj.save()
    custcartobj=cart.objects.filter(custCartForeign=custobj.id)
    totalbill=0
    for i in custcartobj:
        totalbill+=i.totalAmount

# ====================rayzorpay========================
    razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
 
 

    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '../homeMade'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    # ===================================email===============================
    from django.core.mail import EmailMessage
    sm=EmailMessage('order places','order placed from Home Made Food Delivery. Total bill for your order is '+str(totalbill),to=['nayakshivam1@gmail.com'])
    sm.send()
    return render(request,"showloc.html",{'custAddrObj':custAddrObj,'totalbill':totalbill,'session':custsession,'orderobj':orderobj})


def paymentsuccess(request):
    session=request.session['sessionname']
    odata=request.GET.get('order_id')
    print("order data",odata)
    data=request.GET.get('payment_id')
    print(data)
    print(request.GET.get('session'))
    request.session['sessionval']=request.GET.get('session')
    em=request.session['sessionval']
    print(em)
    custobj=Customers1.objects.get(c_email=em)
    cartobj=cart.objects.filter(custCartForeign=custobj.id)
    orderobj=order.objects.get(ordernumber=odata)
    paymentobj=payment(customerid=custobj,oid=orderobj,paymentstatus="paid",transactionid=data,paymentmode='razorpay')
    paymentobj.save()
    for i in cartobj:
        print(i)
        orderdetailobj=orderdetail(ordernumber=odata,customerid=custobj,cartid=i.foodUploadForeign,quantity=i.quantity,totalprice=i.totalAmount,paymentid=paymentobj)
        orderdetailobj.save()
        i.delete()

    
    return render(request,'paymentsuccess.html',{'em':em,'paymentobj':paymentobj,'session':session})

def logout(request):
    del(request.session['sessionval'])
    del(request.session['sessionname'])
    return redirect('../homeMade')

def newtemplate(request):
    custobj=Customers1.objects.all()
    return render(request,'newtemplate.html',{'custobj':custobj})



        
        
        
    
        

           











