from django.conf import settings

PUBLIC_SETTINGS = { s: getattr(settings,s,None) for s in getattr(settings,"PUBLIC_SETTINGS",[]) }

def public_settings(request):
  return {
    'settings': settings,
  }
