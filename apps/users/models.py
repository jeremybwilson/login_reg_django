from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import re, bcrypt

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def validate_and_create_user(self, form_data):
    # def custom_registration_validator(self, form_data):
        errors = []

        first_name = form_data['first_name']
        last_name = form_data['last_name']
        email = form_data['email']
        password = form_data['password']
        confirm_password = form_data['confirm_password']

        if len(first_name) < 1:
            errors.append('Name cannot be blank.')
        if len(first_name) < 2:
            errors.append('Name must be longer than 2 characters.')        
        if len(last_name) < 1:
            errors.append('Username cannot be blank.')
        if len(last_name) < 2:
            errors.append('Username must be longer than 2 characters.')
        if len(email) < 1:
            errors.append('Email cannot be blank.')
        elif not EMAIL_REGEX.match(email):
            errors.append('You must enter a valid email address!')
        if len(password) < 1:
            errors.append('Password cannot be blank.')
        if len(password) < 3:
            errors.append('Password must be at least 3 characters long.')
        if len(confirm_password) < 1:
            errors.append('Confirm password cannot be blank.')
        if password != confirm_password:
            errors.append('Passwords do not match!')

        # create variable to store emails in database
        email_list = User.objects.filter(email=email)

        # error check to validate if email already exists in the db
        if len(email_list) > 0:
            errors.append('Account already in use.  Please choose another.')

        try:
            user = User.objects.get(email=email)
            errors.append('Email already in use.  Please choose another')
            return (False, errors)
        except:
            # if any form field validations are triggered
            if len(errors) > 0:
                # then return error messages back to Registration form
                return (False, errors)
            else:
                # REMEMBER TO HASH THE PASSWORD - using bcrypt library
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                user = User.objects.create(first_name=first_name, last_name=last_name, email=email, pw_hash=pw_hash, permission_level="STUDENT")
                return (True, user.id)

        return (True, user.id)

    def validate_and_update_user(self, user_id, form_data):
        errors = []

        first_name = form_data['first_name']
        last_name = form_data['last_name']
        email = form_data['email']

        if len(first_name) < 2:
            errors.append('First name must be at least 2 characters')
        if len(last_name) < 2:
            errors.append('Last name must be at least 2 characters')
        if not EMAIL_REGEX.match(email):
            errors.append('Must use a valid email address')

        if errors:
            return (False, errors)

        try:
            user = self.get(id=user_id)
            user.first_name = form_data['first_name']
            user.first_name = form_data['last_name']
            user.email = form_data['email']
            user.save()
            return (True, user)
        except:
            errors.append("User doesn't exist")
            return (False, errors)

    def login_user(self, form_data):
        errors = []

        # username = form_data['username']
        email = form_data['email']
        password = form_data['password']

        try:
            # assign user to variable based on POST'ed email address
            user = User.objects.get(email=email)
            # check to see if passwords match
            if not bcrypt.checkpw(password.encode(), user.pw_hash.encode()):
                errors.append('Email or password is invalid')
                return (False, errors)
                print "Errors occurred during password validation"

            # username_list = User.objects.filter(username=username)

            return (True, user.id)
        except:
            errors.append('Email or password is invalid')
            return (False, errors)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=500)
    permission_level = models.CharField(max_length=255)
    udpated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        # return self.email
        output = "<User object: {} {} {}>".format(self.first_name, self.last_name, self.email, self.permission_level)
        return self.output
