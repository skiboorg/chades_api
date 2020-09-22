import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import create_random_string
from .serializers import *
from .models import User
from rest_framework import generics


class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(json.loads(request.data['userData']))
        print(request.FILES)
        serializer = UserSerializer(user, data=json.loads(request.data['userData']))
        if serializer.is_valid():
            serializer.save()
            for f in request.FILES.getlist('avatar'):
                user.avatar = f
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