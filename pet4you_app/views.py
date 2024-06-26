from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout
from django.db.models import Q
from .models import Pet
from .models import Report
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .forms import PetFilterForm
from .forms import VaccineForm
from django.utils import timezone
from datetime import timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.conf import settings
import os
import urllib.request
from PIL import Image as PILImage
import platform
if platform.system() == "Windows":
    from winotify import Notification
    import winreg
else:
    Notification = None

def new_notification(msg):
    print(f"Notification: {msg}")
    if Notification:
        notificacao = Notification(app_id="Pet4You", title=msg)
        notificacao.show()


def notify_new_pets_last_24_hours():
    now = timezone.now()
    ultimas_24horas = now - timedelta(hours=24)
    new_pets_count = Pet.objects.filter(created_at__gte=ultimas_24horas).count()
    print(f"Número de pets criados nas últimas 24 horas: {new_pets_count}")
    if Notification:
        new_notification(f"Número de pets criados nas últimas 24 horas: {new_pets_count}")
    
@csrf_exempt
@require_POST
def create_admin_user(request):
    username = "anton"
    password = "123456"
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username=username, email='admin@example.com', password=password)
        user.save()
        return JsonResponse({'status': 'admin_created'})
    else:
        return JsonResponse({'status': 'admin_exists'})
    
def download_pet(request,pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pet.name}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Título
    title = "Informações do Pet"
    p.setFont("Helvetica-Bold", 20)
    text_width = p.stringWidth(title, "Helvetica-Bold", 20)
    p.drawString((width - text_width) / 2, height - 50, title)

    # Imagem
    if pet.photo:
        photo_url = pet.photo
        
        try:
            image = ImageReader(photo_url)
            p.drawImage(image, (width - 150) / 2, height - 250, width=150, height=150)
        except Exception as e:
            print(f"Error loading image from URL: {e}")
            p.setFont("Helvetica", 12)
            #p.drawString(100, height - 250, "Imagem não disponível")
            text_width = p.stringWidth("Imagem não disponível", "Helvetica-Bold", 20)
            p.drawString((width - text_width) / 2, height - 250, "Imagem não disponível")
            

    # Detalhes
    p.setFont("Helvetica-Bold", 12)
    y_position = height - 340
    p.drawString(100, y_position, f"Nome: {pet.name}")
    p.setFont("Helvetica", 12)
    p.drawString(100, y_position - 30, f"Espécie: {pet.species}")
    p.drawString(100, y_position - 60, f"Raça: {pet.breed}")
    p.drawString(100, y_position - 90, f"Idade: {pet.age}")
    p.drawString(100, y_position - 120, f"Descrição: {pet.description}")

    p.showPage()
    p.save()

    return response
    
def vaccine_card(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    vaccines = pet.vaccines.all()
    return render(request, 'vaccine_card.html', {'pet': pet, 'vaccines': vaccines})

def vaccine_add(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    if request.method == 'POST':
        form = VaccineForm(request.POST)
        if form.is_valid():
            vaccine = form.save(commit=False)
            vaccine.pet = pet
            vaccine.save()
            return redirect('pet4you:vaccine_card', pet_id=pet.id)
    else:
        form = VaccineForm()
    
    return render(request, 'vaccine_add.html', {'form': form, 'pet': pet})

def createPost(request):
   p = Pet.objects.all()
   if(request.method == 'POST'):
       name = request.POST.get('name')
       species = request.POST.get('species')
       breed = request.POST.get('breed')
       age = request.POST.get('age')
       description = request.POST.get('description')
       photo = request.POST.get('photo')
       owner = request.user
       
       #Validation:
       errors = {}
       if not photo:
            errors['photo'] = 'Photo is required.'
       if not name:
            errors['name'] = 'Name is required.'
       if not age:
            errors['age'] = 'Age is required.'
       if not breed:
            errors['breed'] = 'Breed is required'
       if not species:
            errors['species'] = 'Species is required'
       if age != '':
           if int(age) > 99:
             errors['age'] = 'Age has to be under 99'

       if errors:
            return render(request, 'posting.html', {'errors': errors})
        
       pet = Pet(name=name, species=species,breed=breed,age=age,description=description, photo=photo,created_at='',owner=owner,favorited=False)
       pet.save()
       new_notification("Post adicionado com sucesso!")
       return redirect("pet4you:home")
   else:
       return render(request, 'posting.html')

def favoritar_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if(pet.favorited == False):
        new_notification("Post favoritado com sucesso")
        pet.favorited = True
    else:
        new_notification("Post desfavoritado com sucesso")
        pet.favorited = False
    pet.save()
    return redirect('pet4you:home')

def desfavoritar_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.favorited = False
    pet.save()
    new_notification("Post desfavoritado com sucesso")
    return redirect('pet4you:favorite')

def listPets(request):
    user = request.user 
    pets = Pet.objects.filter(owner=user)
    return render(request, 'list.html', {'pets': pets})

def listFavorites(request):
    user = request.user 
    pets = Pet.objects.filter(favorited=True)
    return render(request, 'favorite.html', {'pets': pets})

def add_report(request, pet_id):
    reports = Report.objects.all()
    pet = get_object_or_404(Pet, pk=pet_id)
    if(request.method == 'POST'):
        text = request.POST.get('text')
        reporter = request.user
        report = Report(reporter=reporter,pet=pet, text=text)
        report.save()
        new_notification("Post reportado com sucesso")
        return redirect("pet4you:home")
    else:
        return render(request, 'report.html', {'pet': pet})

def report_admin_view(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    pet = report.pet
    return render(request, 'report_admin.html', {'report': report, 'pet': pet})



def list_reports(request):
    reports = Report.objects.all()
    return render(request, 'report_list.html', {'reports' : reports} )


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                notify_new_pets_last_24_hours()
                return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            notify_new_pets_last_24_hours()
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout(request):
    auth_logout(request)
    new_notification("Logout Realizado")
    return redirect('home')


def home(request):
    species = request.GET.get('especie')
    breed = request.GET.get('raca')
    name = request.GET.get('nome')
    age = request.GET.get('idade')

    pets_para_adocao = Pet.objects.all()

    if species:
        pets_para_adocao = pets_para_adocao.filter(species=species)
    if breed:
        pets_para_adocao = pets_para_adocao.filter(breed=breed)
    if name:
        pets_para_adocao = pets_para_adocao.filter(name=name)
    if age:
        pets_para_adocao = pets_para_adocao.filter(age=age)

    return render(request, 'home.html', {'pets_para_adocao': pets_para_adocao})

def edit_post(request, pet_id):
  
    pet = get_object_or_404(Pet, pk=pet_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        age = request.POST.get('age')
        description = request.POST.get('description')
        photo = request.POST.get('photo')
        owner = request.user
        
         #Validation:
        errors = {}
        if not photo:
            errors['photo'] = 'Photo is required.'
        if not name:
            errors['name'] = 'Name is required.'
        if not age:
            errors['age'] = 'Age is required.'
        if not breed:
            errors['breed'] = 'Breed is required'
        if not species:
            errors['species'] = 'Species is required'
        if age != '':
           if int(age) > 99:
             errors['age'] = 'Age has to be under 99'

        if errors:
            return render(request, 'edit_post.html', {'errors': errors, 'pet': pet})
        
        pet.name = name
        pet.species = species
        pet.breed = breed
        pet.age = age
        pet.description = description
        pet.photo = photo
        
        pet.save()
        new_notification("Post editado com sucesso")
        return redirect("pet4you:home")
    else:
        return render(request, 'edit_post.html', {'pet': pet})

def listar_pets(request):
    pets = Pet.objects.all()
    return render(request, 'listarpet.html', {'pets': pets})

@login_required
def delete_post(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.user == pet.owner or request.user.is_superuser:
        pet.delete()
        return redirect('pet4you:home')
    else:
        return redirect('pet4you:home')

@login_required
def delete_post_as_user(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    user = request.user

    pets = Pet.objects.filter(owner=user)
    pet.delete()
    return render(request, 'list.html', {'pets': pets})


@login_required
def adopt_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    user = request.user
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        cpf = request.POST.get('cpf')
        birth_date = request.POST.get('birth_date')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        number = request.POST.get('number')
        complement = request.POST.get('complement', '')
        neighborhood = request.POST.get('neighborhood')
        state = request.POST.get('state')
        city = request.POST.get('city')

        # Aqui você pode adicionar validações manuais se necessário
        if not all([full_name, cpf, birth_date, email, phone, address, number, neighborhood, state, city]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
        else:
            pet.owner = user
            pet.adopted = True
            pet.adoption_date = timezone.now()
            pet.save()
            new_notification("Solicitação feita com sucesso!")
            messages.success(request, 'Você adotou o pet com sucesso!')
            return redirect("pet4you:home")
    
    return render(request, 'adopt.html', {'pet': pet})
