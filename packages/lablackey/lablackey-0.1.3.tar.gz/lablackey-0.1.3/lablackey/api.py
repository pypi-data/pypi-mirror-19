from django.apps import apps
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers

def get_model(app_name,model_name):
  return apps.get_app_config(app_name).get_model(model_name)

def get_one(request,app_name,model_name,pk):
  model = get_model(app_name,model_name)
  obj = get_object_or_404(model,pk=pk)
  if not obj.row_permissions(request.user):
    raise NotImplementedError
  return JsonResponse(obj.as_json)

def get_many(request,app_name,model_name):
  model = get_model(app_name,model_name)
  kwargs = {k: request.GET[k] for k in model.filter_fields if k in request.GET}
  objs = model.objects.filter(**kwargs)
  if not [obj.row_permissions(request.user) for obj in objs]:
    raise NotImplementedError
  return JsonResponse([o.as_json for o in objs],safe=False)
