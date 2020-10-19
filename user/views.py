import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import create_random_string
from .serializers import *
from .models import User
from rest_framework import generics


class AddPoints(APIView):
    def post(self,request):
        print(request.data)
        request.user.score+=int(request.data['points'])
        request.user.save()
        return  Response(status=200)

class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(json.loads(request.data['userData']))
        print(request.FILES)
        data = json.loads(request.data['userData'])
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            for f in request.FILES.getlist('avatar'):
                user.avatar = f
                user.save()
            if data['password1'] and data['password1'] == data['password2']:
                user.set_password(data['password1'])
                user.save()
            return Response(status=200)

        else:
            print(serializer.errors)
            return Response(status=400)

class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user
    # def get(self, request):
    #     user = request.user
    #     serializer = UserSerializer(user, many=False)
    #     return Response(serializer.data)

class getUserEmailbyPhone(APIView):
    def post(self,request):
        print(request.data)
        user = None
        try:
            user = User.objects.get(phone=request.data['phone'])
        except:
            user= None
        if user:
            return Response({'result': True, 'email': user.email},status=200)
        else:
            return Response(status=404)

class GetAllAchives(generics.ListAPIView):
    queryset = Achive.objects.all()
    serializer_class = AchivesSerializer