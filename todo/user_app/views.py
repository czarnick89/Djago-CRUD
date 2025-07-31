from django.shortcuts import render
from .models import TodoUser
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as s
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class SignUpView(APIView):
    def post(self, request):
        request.data["username"] = request.data["email"]
        todo_user = TodoUser.objects.create_user(**request.data)
        #print(todo_user)
        token_obj = Token.objects.create(user=todo_user)
        return Response(
            {"todo_user": todo_user.email, "token": token_obj.key}, status=s.HTTP_201_CREATED)

class LogInView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        todo_user = authenticate(username=email, password=password)
        if todo_user:
            token, created = Token.objects.get_or_create(user=todo_user)
            return Response({"token": token.key, "todo_user": todo_user.email})
        else:
            return Response("No todo_user matching credentials", status=s.HTTP_404_NOT_FOUND)

class LogOutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response("User sucessfully logged out.", status=s.HTTP_204_NO_CONTENT)

class UpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user

        old_password = request.data.get('old_password')
        if not old_password:
            return Response("Old password is required.", status=s.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response("Invalid old password.", status=s.HTTP_401_UNAUTHORIZED)

        # Update fields
        for field in ['age', 'display_name', 'address']:
            if value := request.data.get(field):
                setattr(user, field, value)

        # Password change
        new_password = request.data.get("new_password")
        if new_password:
            user.set_password(new_password)

        user.save()
        return Response("User updated.", status=s.HTTP_200_OK)
