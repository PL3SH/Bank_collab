from django.http import Http404
from django.contrib.auth import logout
from .models import Client, Account
import requests
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import EmailForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Client
import cv2
import os
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import ClientForm





from django.shortcuts import render

def create_client(request):
    return render(request, 'create_client.html')


@login_required
def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            # Extrae datos del formulario
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # URL del logo
            logo_url = f"{settings.STATIC_URL}images/logo.png"

            # Renderiza el contenido HTML del correo
            html_content = render_to_string('emails/send_email_template.html', {
                'logo_url': logo_url,
                'subject': subject,
                'message': message,
            })

            # Configura y envía el correo
            email = EmailMultiAlternatives(
                subject=subject,
                body=message,  # Versión en texto plano
                from_email=settings.EMAIL_HOST_USER,
                to=[recipient_email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            return redirect('/email-sent-success/')  # Redirige a la página de éxito
    else:
        form = EmailForm()

    return render(request, 'send_email_form.html', {'form': form})

@login_required
def sent_email_success(request):
    return render(request, 'email_sent_success.html')


def home(request):
    return render(request, 'index.html')
@login_required
def asesores(request):
    return render(request, 'asesores.html')
@login_required
def educacion(request):
    return render(request, 'educacion_financiera.html')
@login_required
def negocios(request):
    return render(request, 'negocios.html')

def pqr(request):
    return render(request, 'pqr.html')
@login_required
def tramites(request):
    return render(request, 'tramites_digitales.html')
def blog(request):
    return render(request, 'blog.html')

@login_required


def bin_lookup(request):
    card_data = None
    error = None

    if request.method == 'POST':
        bin_number = request.POST.get('bin_number')
        if bin_number:
            # URL de la API
            api_key = settings.BIN_CHECKER_API_KEY
            url = f"https://api.bincodes.com/bin/?format=json&api_key={api_key}&bin={bin_number}"
            
            # Hacer la solicitud a la API
            try:
                response = requests.get(url)
                response.raise_for_status()  # Asegura que no haya error HTTP
                data = response.json()
                print(data)
                # Verifica si la respuesta contiene datos válidos
                if data.get("valid") == "true":
                    card_data = data
                else:
                    error = "El BIN ingresado no es válido o no se encuentra en la base de datos."

            except requests.exceptions.RequestException as e:
                error = f"Ocurrió un error al hacer la solicitud: {str(e)}"

    return render(request, 'card_info.html', {'card_data': card_data, 'error': error})



@login_required
def client_list(request):
    clients = Client.objects.all() #Busca todos los clientes que se encuentren, sin verificar estatus
    
    return render(request, 'client/client_list.html', {'clients': clients})
def create_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES)  # Si capturas imagen, usa request.FILES
        if form.is_valid():
            form.save()
            return redirect('blog:client_list')  # Redirigir a la lista de clientes
    else:
        form = ClientForm()
    return render(request, 'create_client.html', {'form': form})

@csrf_exempt
def capture_image(request):
    if request.method == "POST":
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return JsonResponse({'error': 'No se pudo abrir la cámara'})
        ret, frame = cam.read()
        cam.release()

        if not ret:
            return JsonResponse({'error': 'No se pudo capturar la imagen'})
        
        _, buffer = cv2.imencode('.jpg', frame)
        image_data = buffer.tobytes()
        
        # Convertir la imagen a base64 para previsualización
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        # Guardar la imagen en un archivo temporal
        image_file = ContentFile(image_data, name="captured_image.jpg")

        # Crear un nuevo cliente solo para pruebas (puedes eliminar esto después)
        client = Client.objects.create(name="Cliente Prueba", imageSave=image_file)
        
        return JsonResponse({'image_data': image_base64, 'image_url': client.imageSave.url})
    
    return JsonResponse({'error': 'Método no permitido'})


@login_required
def client_detail(request, id):
    try:
        client = Client.objects.get(id=id)
        # Verificar si el cliente tiene una cuenta asociada
        if hasattr(client, 'account'):
            account_number = client.account.numberAccount  # Acceder al número de cuenta correctamente
            model = client.account.get_account_type_display
        else:
            account_number = 'No Account'  # Si no tiene una cuenta
    except Client.DoesNotExist:
        raise Http404("Client not found")
    loans = Loan.objects.filter(client=client)  # Obtener todos los préstamos del cliente

    # Suponiendo que deseas mostrar solo un monto total de deuda
    total_debt = sum(loan.amount for loan in loans)

    context = {
        'client': client,
        'total_debt': total_debt,
        'loans': loans,
    }
    
    return render(request, 'client/client_detail.html', {'client': client, 'account_number': account_number, 'model': model,})


# Vista de registro de usuario
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso, has iniciado sesión.")
            return redirect("blog:home")
        else:
            messages.error(request, "Error al registrarse. Verifica los datos.")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

# Vista de login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido, {username}")
                return redirect("blog:home")
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request) 
    return redirect('blog:home') 

from django.shortcuts import render, get_object_or_404, redirect
from .models import Loan
from .forms import LoanForm
from django.contrib.auth.decorators import login_required

@login_required
def loan_list(request):
    loans = Loan.objects.all()
    return render(request, 'loan/loan_list.html', {'loans': loans})

@login_required
def loan_detail(request, id):
    loan = get_object_or_404(Loan, id=id)
    return render(request, 'loan/loan_detail.html', {'loan': loan})

@login_required
def loan_create(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:loan_list')
    else:
        form = LoanForm()
    return render(request, 'loan/loan_form.html', {'form': form})

@login_required
def loan_update(request, id):
    loan = get_object_or_404(Loan, id=id)
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            return redirect('blog:loan_detail', id=id)
    else:
        form = LoanForm(instance=loan)
    return render(request, 'loan/loan_form.html', {'form': form})

@login_required
def loan_delete(request, id):
    loan = get_object_or_404(Loan, id=id)
    if request.method == 'POST':
        loan.delete()
        return redirect('blog:loan_list')
    return render(request, 'loan/loan_confirm_delete.html', {'loan': loan})
