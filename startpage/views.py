from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm

# Create your views here.
def home(request):
    return render(request, 'startpage/home.html')

def contact(request):
    form = ContactForm()
    if request.method == "POST" :
        contacts = ContactForm(request.POST)
        if contacts.is_valid():
            userObj = contacts.cleaned_data
            name = userObj['name']
            email = userObj['email']
            message = userObj['message']
            Contact.objects.create(name = name, email = email, message = message)
            return redirect('/#success')
        else:
            return redirect('/#contact')
    else:
        return redirect('/#contact')