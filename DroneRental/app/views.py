from .models import Drone
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Order
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def home(request):
    return render(request,"index.html")

def logout_view(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('home')) 

#superuser admin paneli için
def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser)
def adminpanel(request):
    return render(request,"adminpanel.html")

def rentalrecords(request):
    orders = Order.objects.all() 
    return render(request, "rentalrecords.html", {"orders": orders})

@user_passes_test(is_superuser)
def ihalist(request):
    drone_objects = Drone.objects.all().order_by('id')  # id alanına göre en yüksekten en düşüğe doğru sıralama yapar

    # Paginator
    paginator = Paginator(drone_objects, 7)  # 8 elemanlık sayfalar oluşturacak şekilde ayarlandı.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Paginator

    context = {
        'page_obj': page_obj  # Sayfalama için kullanılacak verileri context içine eklendi.
    }
    return render(request, 'ihalist.html', {'page_obj': page_obj})

@user_passes_test(is_superuser)
def ihaedit(request, drone_id):
    drone = get_object_or_404(Drone, pk=drone_id)
    context = {
        'drone': drone
    }
    return render(request, 'ihaedit.html', context)

#Yapılan değişiklikleri veritabanına kaydetme
def ihaedit_save(request, drone_id):
    # Drone objesini veritabanından al
    drone = get_object_or_404(Drone, pk=drone_id)
    
    if request.method == 'POST':
        # POST isteğiyle gelen form verilerini al
        drone.name = request.POST.get('name')
        drone.category = request.POST.get('category')
        drone.description = request.POST.get('description')
        drone.brand = request.POST.get('brand')
        drone.model = request.POST.get('model')
        drone.weight = request.POST.get('weight')
        drone.price = request.POST.get('price')
        
        # Drone nesnesini kaydet
        drone.save()
        
        # Başarılı bir şekilde kaydedildikten sonra ihalist sayfasına yönlendir
        return redirect('ihalist')
    
    # Eğer form post edilmediyse veya form doğru bir şekilde işlenmediyse, tekrar düzenleme sayfasını göster
    return render(request, 'ihaedit.html', {'drone': drone})


def ihadelete(request, drone_id):
    if request.method == 'POST':
        # Drone objesini veritabanından al veya 404 hatası döndür
        drone = get_object_or_404(Drone, pk=drone_id)
        drone.delete() 
        return redirect('ihalist')
    
@user_passes_test(is_superuser)
def ihaadd(request):
    if request.method == 'POST':
        # POST isteğiyle gelen form verilerini al
        name = request.POST.get('name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        weight = request.POST.get('weight')
        price = request.POST.get('price')
        
        # En son id değerini al
        last_id = Drone.objects.order_by('-id').first().id
        
        # Formdan gelen verilerle yeni bir Drone nesnesi oluştur
        new_drone = Drone(
            id=last_id + 1,  # En son id değerine 1 ekleyerek yeni id değerini atıyoruz
            name=name,
            category=category,
            description=description,
            brand=brand,
            model=model,
            weight=weight,
            price=price
        )
        
       
        new_drone.save()
        
       
        return redirect('ihalist')
    
    # Eğer form post edilmediyse veya form doğru bir şekilde işlenmediyse, ihaadd sayfasını göster
    return render(request, 'ihaadd.html')


def listforuser(request):
    drone_objects = Drone.objects.all().order_by('id')  # id alanına göre en yüksekten en düşüğe doğru sıralama yapar

    # Paginator
    paginator = Paginator(drone_objects, 7)  # 8 elemanlık sayfalar oluşturacak şekilde ayarlandı.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Paginator

    context = {
        'page_obj': page_obj  # Sayfalama için kullanılacak verileri context içine eklendi.
    }
    return render(request, 'listforuser.html', {'page_obj': page_obj})



def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if user.is_superuser:
                return redirect('adminpanel')  # Süper kullanıcıysa yönetim paneline yönlendir
            else:
                return redirect('home')  # Diğer kullanıcılar için ana sayfaya yönlendir
        else:
            # Giriş başarısız mesajı ya da başka bir işlem
            return render(request, 'loginpage.html', {'error_message': 'Kullanıcı adı veya şifre hatalı'})
    else:
        # GET isteği, yani kullanıcı ilk defa giriş sayfasını görüntülüyor
        if request.user.is_authenticated:
            # Kullanıcı zaten oturum açmışsa, ana sayfaya yönlendir
            if request.user.is_superuser:
                return redirect('adminpanel')
            else:
                return redirect('home')
        else:
            # Oturum açmamışsa, giriş sayfasını göster
            return render(request, 'loginpage.html')
        

def registerpage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
           
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registerpage.html', {'form': form})


def searchresults(request):
    category = request.GET.get('category')
    name = request.GET.get('name')
    brand = request.GET.get('brand')
    weight = request.GET.get('weight')
    price = request.GET.get('price')
    

    # Drone modelinde arama yapmak için filtreleme işlemi
    droneler = Drone.objects.all()
    
    if category:
        droneler = droneler.filter(category__icontains=category)
    
    if name:
        droneler = droneler.filter(name__icontains=name)
    
    if brand:
        droneler = droneler.filter(brand__icontains=brand)
    
    if weight:
        droneler = droneler.filter(weight__icontains=weight)
    
    if price:
        droneler = droneler.filter(price__icontains=price)
    
   
    context = {'droneler': droneler}
    return render(request, 'searchresult.html', context)


def rentdrone(request, drone_id): 
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Bu işlemi gerçekleştirebilmek için oturum açmalısınız.")  
    user = User.objects.get(pk=request.user.pk)
    
    rental_start_datetime = timezone.now()
    rental_end_datetime = rental_start_datetime + timedelta(days=2)

    try:
        order = Order.objects.create(
            drone_id=drone_id,
            user_id=user.id,
            renter_member=user.username,
            rental_start_datetime=rental_start_datetime,
            rental_end_datetime=rental_end_datetime
        )
        
    except Exception as e:
        error_message = f"Drone kiralama işlemi sırasında bir hata oluştu: {str(e)}"
        print(error_message)  
        return render(request, 'errorpage.html', {'error_message': error_message})

    return redirect('home')

def rented_drone_page(request):
    orders = Order.objects.filter(user=request.user)

    context = {'orders': orders}
    return render(request, 'renteddrones.html', context)

def delete_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        order.delete()
        return redirect('renteddrones')  # Silme işleminden sonra orders sayfasına yönlendirme yapabilirsiniz
    else:
        return render(request, 'error.html') 