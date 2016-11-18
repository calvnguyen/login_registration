from __future__ import unicode_literals

from django.db import models
import re
from django.contrib import messages
import bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# name cannot contain numbers
NAME_REGEX = re.compile(r'^[^0-9]+$')
# requires a password to have at least 1 uppercase letter and 1 numeric value.
PASS_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d).+$')

# Create your models here.

class UserManager(models.Manager):
	def login(self, email, password):
		errors = {}

		errors['email-error'] = []
		errors['password-error'] = []

		if len(email) < 1:
			errors['email-error'].append("Email cannot be empty!")

		elif not EMAIL_REGEX.match(email):
			errors['email-error'].append("Invalid email address format!")

		if len(password) < 1:
			errors['password-error'].append("Password cannot be empty!")

		elif len(password) < 8:
			errors['password-error'].append("Password\'s length has to be more than 8 characters!")


		if len(errors['email-error']) != 0 or len(errors['password-error']) != 0:
			return (False, errors)
	
		else:
			try:
				user = User.userMgr.filter(email=email)

				if not bcrypt.hashpw(password, user[0].password.encode('utf-8')) == user[0].password:
					print "login check - password DO NOT MATCH"
					errors['password-error'].append("Either email/pw is incorrect")	
					return (False, errors)
				elif bcrypt.hashpw(password, user[0].password.encode('utf-8')) == user[0].password:
				 	print "login check - passwords match"
	         		return (True, user)


			except User.DoesNotExist:
				errors['email-error'].append("Email cannot be found")
            	return (False, errors)


	def register(self, first_name, last_name, email, password, passwordconfirm, dob):
		errors = {}
		present = datetime.now()
		errors['first-name-error'] = []
		errors['last-name-error'] = []
		errors['email-error'] = []
		errors['dob-error'] = []
		errors['password-error'] = []
		errors['password-confirm-error'] = []


		if len(first_name) < 1:
			errors['first-name-error'].append("First name cannot be empty!")

		elif len(first_name) < 2:
			errors['first-name-error'].append("First name has to be at least 2 characters!")

		elif not NAME_REGEX.match(first_name):
			errors['first-name-error'].append("First name cannot contain a number!")

		if len(last_name) < 1:
			errors['last-name-error'].append("Last name cannot be empty!")

		elif len(last_name) < 2:
			errors['last-name-error'].append("Last name has to be at least 2 characters!")

		elif not NAME_REGEX.match(last_name):
			errors['last-name-error'].append("Last name cannot contain a number!")

		if len(email) < 1:
			errors['email-error'].append("Email cannot be empty!")

		elif not EMAIL_REGEX.match(email):
			errors['email-error'].append("Invalid email address format!")

		elif not self.is_date(dob):
			errors['dob-error'].append("Birthday entered is not valid!!")
		elif datetime.strptime(dob, "%Y-%m-%d") > present:
			errors['dob-error'].append("Birthday must be from the past!")

		if len(password) < 1:
			errors['password-error'].append("Password cannot be empty!")

		elif len(password) < 8:
			errors['password-error'].append("Password's length has to be more than 8 characters!")

		elif not PASS_REGEX.match(password):
			errors['password-error'].append("Password needs to have at least 1 number and 1 Upper-Case letter!")

		
		if len(passwordconfirm) < 1:
			errors['password-confirm-error'].append("Password Confirmation cannot be empty!")

		elif not PASS_REGEX.match(passwordconfirm):
			errors['password-confirm-error'].append("Password confirmation needs to have at least 1 number and 1 Upper-Case letter!")
		
		elif len(passwordconfirm) < 8:
			errors['password-confirm-error'].append("Password confirmation's length has to be more than 8 characters!")
		
		if password != passwordconfirm:
			errors['password-confirm-error'].append("Password and password's confirmation must match!")

		print len(errors['email-error'])
		if len(errors['email-error']) != 0 or len(errors['password-error']) != 0 or len(errors['password-confirm-error']) != 0 or len(errors['dob-error']) != 0 or len(errors['first-name-error']) != 0 or len(errors['last-name-error']) != 0:
			return (False, errors)
		
		else:				
			user = User.userMgr.filter(email = email)
			if (user):
				errors['email-error'].append("Email already exists. Please proceed to login or choose another one")
				return (False, errors)
			else:
				hashed = bcrypt.hashpw(password, bcrypt.gensalt().encode('utf-8'))
				user = User.userMgr.create(first_name=first_name, last_name=last_name, email=email, password=hashed, dob=dob)
				user.save()
				return (True, user)

	def is_date(self, birthday):
		try:
			if birthday != datetime.strptime(birthday, "%Y-%m-%d").strftime('%Y-%m-%d'):
				raise ValueError
			return True
   		except ValueError:
			return False

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	dob = models.CharField(max_length=10, null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	userMgr = UserManager()