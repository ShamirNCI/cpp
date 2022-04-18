from django.shortcuts import get_object_or_404, render
from decimal import Decimal

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Bus, Book ,Asset,AssetMain
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
id_g = 0
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def home(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    else:
        return render(request, 'myapp/signin.html')


@login_required(login_url='signin')
def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        bus_list = Bus.objects.filter(source=source_r, dest=dest_r, date=date_r)
        if bus_list:
            return render(request, 'myapp/list.html', locals())
        else:
            context["error"] = "Sorry no buses availiable"
            return render(request, 'myapp/findbus.html', context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=id_r)
        if bus:
            if bus.rem > int(seats_r):
                name_r = bus.bus_name
                cost = int(seats_r) * bus.price
                source_r = bus.source
                dest_r = bus.dest
                nos_r = Decimal(bus.nos)
                price_r = bus.price
                date_r = bus.date
                time_r = bus.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = bus.rem - seats_r
                Bus.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, bus_name=name_r,
                                           source=source_r, busid=id_r,
                                           dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                # book.save()
                return render(request, 'myapp/bookings.html', locals())
            else:
                context["error"] = "Sorry select fewer number of seats"
                return render(request, 'myapp/findbus.html', context)

    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            #nos_r = book.nos - seats_r
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'myapp/findbus.html', context)

def viewasset(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('asset_id')
        asset_view = Book.objects.filter(userid=id_r)
        #seats_r = int(request.POST.get('no_seats'))
        if asset_view:
            return render(request, 'myapp/booklist.html', locals())
        else:
            context["error"] = "Sorry no buses booked"
            return render(request, 'myapp/findbus.html', context)

    else:
        return render(request, 'myapp/findbus.html')
#@login_required(login_url='signin')
def asset(request,new={}):
    context = {}
    #id_r = request.user.id
    asset = Asset.objects.all()
    #assest_list = Asset.objects.filter(asset_name="Civil")
    if asset:
        return render(request, 'myapp/asset.html', locals())
    else:
        context["error"] = "Sorry no asset record"
        #return render(request, 'myapp/findbus.html', context)


def assetmainlist(request,new={}):
    context = {}
    #id_r = request.user.id
    asset = AssetMain.objects.all()
    #assest_list = Asset.objects.filter(asset_name="Civil")
    if asset:
        return render(request, 'myapp/assetmainlist.html', locals())
    else:
        context["error"] = "Sorry no asset record"
        #return render(request, 'myapp/findbus.html', context)




def assetmainupdate(request,pk,new={}):
    global id_g
    print('s1')
    print(pk)
    asset_main = AssetMain.objects.filter(id=pk)
    print(asset_main)
    asset_id_r= str(request.POST.get('Issue_id'))
    asset_assign_r = str(request.POST.get('asset_assign'))
    date_solved_r = str(request.POST.get('date_solved'))
    asset_comments_r = str(request.POST.get('asset_comments'))
    context = {} 
    if request.method == 'POST' and 'python_code' in request.POST:
        print('python code in')
        AssetMain.objects.filter(id=asset_id_r).update(
        asset_assign =asset_assign_r, asset_comments =asset_comments_r,date_solved=date_solved_r)
    return render(request, 'myapp/assetmainupdate.html', locals())
    #context = {} 
    #id_r = request.POST.get('asset_id')
    # #AssetMain.objects.filter(id=id_r).update(asset_desc='me5')
    # if request.method == 'POST' and 'python_code' in request.POST:
    #     id_r = request.POST.get('asset_id')
    #     id_r = id_g
    #     asset_main = AssetMain.objects.filter(id=id_r)
    #     asset_desc_r = str(request.POST.get('asset_desc'))
    #     AssetMain.objects.filter(id=id_r).update(asset_desc=asset_desc_r)
    #     asset_desc_r = str(request.POST.get('asset_desc'))
    #     print("------")
    #     print(id_g)
    #     print(asset_main)
    #     print(asset_desc_r)
    #     print('python code wor')
    #     print("------")
    if request.method == 'POST':
        id_r = request.POST.get('asset_id')
        #id_r = '71'
        asset_main = AssetMain.objects.filter(id=id_r)
        print('im n')
        print(asset_main)
        #AssetMain.objects.filter(id=id_r).update(asset_desc='me1')
        #AssetMain.objects.filter(id=id_r).update(asset_desc='done')
        #print(asset_main)
        #print(id_r)
        print("elif")
        asset_id_r= str(request.POST.get('Issue_id'))
        asset_name_r = str(request.POST.get('asset_name'))
        asset_tag_r = str(request.POST.get('asset_tag'))
        asset_serial_No_r = str(request.POST.get('asset_serial_No'))
        asset_loc_r = str(request.POST.get('asset_loc'))
        date_main_r = request.POST.get('date_main')
        asset_desc_r = str(request.POST.get('asset_desc'))
        asset_assign_r = str(request.POST.get('asset_assign'))
        date_solved_r = str(request.POST.get('date_solved'))
        asset_comments_r = str(request.POST.get('asset_comments'))
        if 'python_code' in request.POST:
            print('python code in')
            AssetMain.objects.filter(id=asset_id_r).update(
            asset_assign =asset_assign_r, asset_comments =asset_comments_r,date_solved=date_solved_r)


        if asset_main:
            return render(request, 'myapp/assetmainupdate.html', locals())
            print(locals())
        else:
            context["error"] = "Sorry no asset information"
            return render(request, 'myapp/assetmainupdate.html', context)

        if asset_main:
            return render(request, 'myapp/assetmainupdate.html', locals())
            print(locals())
        else:
            context["error"] = "Sorry no asset information"
            return render(request, 'myapp/assetmainupdate.html', context)
       
        #book_list = Asset.objects.filter(asset_id=id_r)
        #seats_r = int(request.POST.get('no_seats'))


    return render(request, "myapp/home.html", {})
def assetview(request,new={}):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('asset_id')
        asset_view = Asset.objects.filter(asset_id=id_r)
        #seats_r = int(request.POST.get('no_seats'))
        if asset_view:
            return render(request, 'myapp/assetview.html', locals())
        else:
            context["error"] = "Sorry no asset information"
            return render(request, 'myapp/assetview.html', context)
    else:
        return render(request, 'myapp/assetview.html')

def assetmain(request,new={}):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('asset_id')
        asset_main = Asset.objects.filter(asset_id=id_r)
        print(id_r)
        asset_id_r= str(request.POST.get('asset_id'))
        asset_name_r = str(request.POST.get('asset_name'))
        asset_tag_r = str(request.POST.get('asset_tag'))
        asset_serial_No_r = str(request.POST.get('asset_serial_No'))
        asset_loc_r = str(request.POST.get('asset_loc'))
        date_main_r = request.POST.get('date_main')
        asset_desc_r = str(request.POST.get('asset_desc'))
        asset_assign_r = str(request.POST.get('asset_assign'))
        date_solved_r = str(request.POST.get('date_solved'))
        asset_comments_r = str(request.POST.get('asset_comments'))
        ##
        print("asset_name_r")
        print(asset_name_r)
        if asset_name_r != 'None':
            assetmain = AssetMain.objects.create(asset_id = asset_id_r,asset_name = asset_name_r, asset_tag =asset_tag_r,
            date_main= date_main_r,asset_serial_No =asset_serial_No_r,asset_loc =asset_loc_r, asset_status ='Open',
            asset_desc =asset_desc_r,asset_assign =asset_assign_r, asset_comments =asset_comments_r)
        # # ##
        print(asset_name_r,asset_tag_r,asset_serial_No_r)
        if asset_main:
            return render(request, 'myapp/assetmain.html', locals())
            print(locals())
        else:
            context["error"] = "Sorry no asset information"
            return render(request, 'myapp/assetmain.html', context)
       
        #book_list = Asset.objects.filter(asset_id=id_r)
        #seats_r = int(request.POST.get('no_seats'))
    return render(request, "myapp/home.html", {})

def index(request):
    if request.method == 'POST':
        var = request.POST.getlist('mylist')
        id_r = request.POST.get('mylist1')
        print(var)
        print(id_r)
    return render(request, "myapp/home.html", {})

def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            return render(request, 'myapp/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/success.html', context)
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)

