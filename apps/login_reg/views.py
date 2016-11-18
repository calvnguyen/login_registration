from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User


# Create your views here.
def index(request):
  if 'user_id' in request.session:
    return redirect("/success")
    request.session['status'] = "logged"
  else:
    return redirect("/login") 

def login(request):

  if request.method == "POST": 
    print "im in Login - Post"
    password = request.POST['password'].encode('utf-8')
    result = User.userMgr.login(request.POST['email'], password)

    if result[0]:
      print result[1]
      request.session['user_id'] = result[1][0].id
      request.session['status'] = "logged"
      return redirect("/success")
    else:
 
      if 'email-error' in result[1]:
        for msg in result[1]['email-error']:
          messages.add_message(request, messages.ERROR, msg, extra_tags='email-error')
      if 'password-error' in result[1]:
        for msg in result[1]['password-error']:
          messages.add_message(request, messages.ERROR, msg, extra_tags='password-error')

    	return redirect("/login")

  elif request.method == "GET":
    	return render(request, 'login_reg/login.html')


def create_user(request):
  
  if (request.method == "GET"):
		return render(request, "login_reg/index.html")

  elif (request.method == "POST"):
    print "Got Post Info"
    password = request.POST['password'].encode('utf-8')
    result = User.userMgr.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'], password, request.POST['passwordconfirm'], request.POST['dob'])
    print "Got out of register"
    if result[0]:
      print "Able to create ok"
      request.session['user_id'] = result[1].id
      request.session['status'] = "registered"
      return redirect('/success')
    else:
      print result[1]
      if 'email-error' in result[1]:
        for msg in result[1]['email-error']:
          messages.add_message(request, messages.ERROR, msg, extra_tags='email-error')
      if 'password-error' in result[1]:
        for msg in result[1]['password-error']:
          messages.add_message(request, messages.ERROR, msg, extra_tags='password-error')
      if 'password-confirm-error' in result[1]:
        for msg in result[1]['password-confirm-error']:
          messages.add_message(request, messages.ERROR, msg, extra_tags='password-confirm-error')
      if 'first-name-error' in result[1]:
        for msg in result[1]['first-name-error']:
          messages.add_message(request, messages.ERROR, msg, extra_tags='first-name-error')
      if 'last-name-error' in result[1]:
        for msg in result[1]['last-name-error']:
          messages.add_message(request, messages.ERROR, msg, extra_tags='last-name-error')
      if 'dob-error' in result[1]:
        for msg in result[1]['dob-error']:
          messages.add_message(request, messages.ERROR, msg, extra_tags='dob-error')

      return redirect('/register')
  else:
    return redirect('/register')

def show(request):

  if 'user_id' in request.session:
    print "my user id", request.session['user_id']
    user_account = User.userMgr.get(id = request.session['user_id'])

    context = {'user_account': user_account}


    return render(request, 'login_reg/success.html', context)

  else:
    return redirect("/login")

def logout(request):
  request.session.pop('user_id')
  return redirect('/login')