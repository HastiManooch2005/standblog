from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def user_login(request):
    #if request.user.is_authenticated == True:#yani ehraz hovat shode va be safeh login nemitanim beravim
        #return redirect('/')#ya / safeh asli

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass")
        #print(name,password)
        user = authenticate(request, username=username, password=password)#aya etelat ke karaber vared mikone etelat an dorost ast ya na
        if user is not None:
            login(request, user)#method amade baray login karadan
            return redirect("/")#hedayat mikone be safeh dige
    return render(request,"account/login.html",context={})


def logout_view(request):
    logout(request)
    return redirect("/")

def register(request):#sabt nam karbar chon karbar jadid vared mishe bayad be database ezafe konim
    context ={'error':[]}
    if request.user.is_authenticated == True:
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass")
        password2 = request.POST.get("pass2")
        email = request.POST.get("email")
        if password != password2:
           context['error'].append("password not true")
        User.objects.create_user(username=username, password=password, email=email)
        redirect("/")
    return render(request,'account/register.html',context={})
