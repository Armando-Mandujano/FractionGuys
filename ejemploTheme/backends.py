from django.contrib.auth.backends import ModelBackend
from frontend.models import Profesor

class ProfesorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            profesor = Profesor.objects.get(email=username)
        except Profesor.DoesNotExist:
            return None
        if profesor.check_password(password):
            return profesor
        return None
