from django.shortcuts import render, redirect
from .models import Member
from .forms import MemberForm
from django.contrib import messages

# Create your views here.
def home(request):
    all_memebers = Member.objects.all()
    return render(request, 'home.html',{'all':all_memebers})

def join(request):
    if request.method == 'POST':
        form = MemberForm(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            passwd = request.POST['passwd']
            age = request.POST['age']
            messages.success(request, ("All fields must be filled to submit the form!"))
            # return redirect('home')
            return render(request, 'join.html',{'fname_value':fname, 'lname_value':lname, 'email_value':email, 'passwd_value':passwd, 'age_value':age,})

        messages.success(request, ("Your form has been Submitted Successfully!"))
        return redirect('home')

    else:
        return render(request, 'join.html',{})