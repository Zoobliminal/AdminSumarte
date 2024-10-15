from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Create your views here.

class vistaRegistro(View):

    def get(self, request):
        
        form=UserCreationForm()
        return render(request, "Autenticacion/registro.html", {"form":form})
    
    
    
    def post(self, request):
        
        form=UserCreationForm(request.POST)
        
        if form.is_valid():
            usuario=form.save()
            login(request, usuario)
            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
                
            return render (request, "Autenticacion/registro.html", {"form":form})
        
        
        
        
def loguear(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get("username")
            contrasena=form.cleaned_data.get("password")
            usuario=authenticate(username=nombre_usuario, password=contrasena)
            if usuario is not None:
                login(request, usuario)
                return redirect('home')
            else:
                messages.error(request, "Usuario no encontrado")
        else:
            messages.error(request, "Usuario no valido") 
            
            
    
    form=AuthenticationForm()
    return render(request, "Autenticacion/login.html", {"form":form})



def cerrar_sesion(request):
    logout(request)
    return redirect('home')  
        
