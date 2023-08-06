from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

import random

def _check(a,b):
  success = sorted(a) == sorted(b)
  if not success:
    raise ValueError("\ndesired: %s \nactual  : %s"%(sorted(a),sorted(b)))
  return success

def check_subjects(subjects,outbox=None):
  if not outbox:
    outbox = mail.outbox
  outbox_subjects = [m.subject.replace(settings.EMAIL_SUBJECT_PREFIX,'') for m in outbox]
  return _check(subjects,outbox_subjects)

def check_recipients(recipients,outbox=None):
  if not outbox:
    outbox = mail.outbox
  outbox_recipients = [m.recipients() for m in outbox]
  return _check(recipients,outbox_recipients)

class ClientTestCase(TestCase):
  """
  A TestCase with added functionality such as user/object creationg, login/logout.
  """
  _passwords = {}
  def login(self,username,password=None):
    if isinstance(username,get_user_model()):
      username = username.username
    self.client.post(reverse('login'),{'username': username,'password': password or self._passwords[username]})
  def _new_object(self,model,**kwargs):
    return model.objects.create(**kwargs)
  def new_user(self,username=None,password=None,**kwargs):
    user = self._new_object(get_user_model(),username=username or "user_"%random.random(),**kwargs)
    self._passwords[user.username] = password = password or "%s"%random.random()
    user.set_password(password)
    user.save()
    return user
