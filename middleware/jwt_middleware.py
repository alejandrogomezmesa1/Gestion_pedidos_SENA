from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse

class JWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = JWTAuthentication()
        try:
            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple is not None:
                request.user, request.auth = user_auth_tuple
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=401)
