from django.db import models

def myapp(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())