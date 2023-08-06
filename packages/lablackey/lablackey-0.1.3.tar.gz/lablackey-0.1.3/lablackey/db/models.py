from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import models
from django.template.defaultfilters import slugify

def _prep_kwargs_with_auth(request,kwargs):
  if request.user.is_authenticated():
    kwargs['user'] = request.user
  else:
    if not request.session.exists(request.session.session_key):
      request.session.create()
    kwargs['session'] = Session.objects.get(session_key=request.session.session_key)
  return kwargs

class UserOrSessionMixin(object):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,related_name="user_%(app_label)s%(class)ss")
  session = models.ForeignKey(Session,null=True,blank=True,related_name="user_%(app_label)s%(class)ss",
                              on_delete=models.SET_NULL)
  session_key = models.CharField(max_length=40,null=True,blank=True)

  @classmethod
  def get_or_create_from_request(clss,request,**kwargs):
    obj = clss.get_or_init_from_request(request,**kwargs)
    if not obj.pk:
      obj.save()
    return obj

  @classmethod
  def get_or_init_from_request(clss,request,**kwargs):
    try:
      return clss.get_from_request(request,**kwargs)
    except clss.DoesNotExist:
      pass

    # need session or user
    kwargs = _prep_kwargs_with_auth(request,kwargs)
    defaults = kwargs.pop("defaults",{})

    #can't make an object with an id, pk, or complex lookup
    kwargs.pop("id","")
    kwargs.pop("pk","")
    for key in kwargs.items():
      if "__" in key:
        kwargs.pop(key,"")

    obj = clss(**kwargs)
    for k,v in defaults.items():
      setattr(obj,k,v)
    return obj

  @classmethod
  def get_from_request(clss,request,**kwargs):
    if 'session_key' in request.GET and request.user.is_authenticated():
      # a preexisting object needs to be moved from session to user
      try:
        obj = clss.objects.get(session_key=request.GET['session_key'])
        obj.session_key = None
        obj.user = request.user
        obj.save()
        return obj
      except clss.DoesNotExist:
        # probably already happened, move along
        pass
    kwargs = _prep_kwargs_with_auth(request,kwargs)
    return clss.objects.get(**kwargs)

class OrderedModel(models.Model):
  order = models.PositiveIntegerField(default=99999)
  def save(self,*args,**kwargs):
    if self.order == 99999:
      self.order = 0
      if self.__class__.objects.count():
        self.order = self.__class__.objects.order_by("-order")[0].order+1
    super(OrderedModel,self).save(*args,**kwargs)
  class Meta:
    abstract = True

def to_base32(s):
  key = '-abcdefghijklmnopqrstuvwxyz'
  s = s.strip('0987654321')
  return int("0x"+"".join([hex(key.find(i))[2:].zfill(2) for i in (slugify(s)+"----")[:4]]),16)

class NamedTreeModel(models.Model):
  name = models.CharField(max_length=64)
  parent = models.ForeignKey("self",null=True,blank=True)
  order = models.FloatField(default=0)
  level = models.IntegerField(default=0)
  def get_order(self):
    if self.parent:
      self.level = self.parent.level + 1
      return to_base32(self.parent.name) + to_base32(self.name)/float(to_base32("zzzz"))
    self.level = 0
    return to_base32(self.name)
  def save(self,*args,**kwargs):
    self.order = self.get_order()
    super(NamedTreeModel,self).save(*args,**kwargs)

  __unicode__ = lambda self: "(%s) %s"%(self.parent,self.name) if self.parent else self.name
  class Meta:
    abstract = True

class SlugModel(models.Model):
  title = models.CharField(max_length=128)
  __unicode__ = lambda self: self.title
  slug = models.CharField(max_length=128,null=True,blank=True,unique=True)
  def save(self,*args,**kwargs):
    self.slug = slugify(self.title)
    if self.__class__.objects.filter(slug=self.slug).exclude(id=self.id):
      self.slug += "-%s"%self.id
    return super(SlugModel,self).save(*args,**kwargs)
  class Meta:
    abstract = True

class UserModel(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  class Meta:
    abstract = True
