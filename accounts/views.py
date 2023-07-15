from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.services import register_service, reset_password_service, reset_password_confirm_service


# Register API
class RegisterAPIView(APIView):
    def post(self, request):
        response = register_service(request.data)
        if response['success']:
            return Response(status=201)
        return Response(response, status=405)


# Reset Password API

class ResetPasswordAPIView(APIView):
    def post(self, request):
        responce = reset_password_service(request)
        if responce['success']:
            return Response({'message': 'sent'})
        return Response(responce, status=404)


# Reset Password Confirm API

class PasswordResetConfirmAPIView(APIView):

    def post(self, request, token, uuid):
        response = reset_password_confirm_service(request, token, uuid)
        if response['success']:
            return Response({'message': 'Password changed'})
        return Response(response, status=400)


# Logout API

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = RefreshToken(request.user)
        token.blacklist()
        return Response(status=200)

# User Order API
