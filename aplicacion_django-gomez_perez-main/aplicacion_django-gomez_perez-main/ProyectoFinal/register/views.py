from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

# Create your views here.

def register(request):
   return render(request,"register/register.html")

class VRegistro(View):
   def get(self,request):
     form=UserCreationForm()
     return render(request,"register/register.html",{"form":form})

   def post(self,request):
      form=UserCreationForm(request.POST)

      if form.is_valid():
         usuario=form.save()
         login(request,usuario)
         return redirect("../home/")
      else:
         for msg in form.error_messages:
            messages.error(request,form.error_messages[msg])
      return render(request,"register/register.html",{"form":form})      




def cerrar_sesion(request):
   logout(request)
   return redirect("nba_stats:home")


def logear(request):
   if request.method=='POST':
      form=AuthenticationForm(request,data=request.POST)
      if form.is_valid():
         nombre_ususario=form.cleaned_data.get("username")
         contraseña=form.cleaned_data.get("password")
         usuario=authenticate(username=nombre_ususario,password=contraseña)
         
         if usuario is not None:
            login(request,usuario)
            return redirect ("nba_stats:home")
         else:
            messages.error(request,"usuario no valido")
      else:
          messages.error(request,"Información Incorrecta")


   form=AuthenticationForm()
   return render(request,"login/login.html",{'form':form})