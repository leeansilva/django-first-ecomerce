from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, InputSerializer, TestUserSerializer, UserListSerializer
from apps.users.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import status

@extend_schema(
        request=InputSerializer,
    )
@api_view(['GET', 'POST'])
def user_api_view(request):
    if request.method == 'GET':
        # #? request.data es un diccionario
        # test_data = {
        #     'name':'leansilva',
        #     'email':''
        # }
        # test_user =TestUserSerializer(data=test_data) 
        # if test_user.is_valid():
        #     print('Pasó validaciones.')
        # else:
        #     #? 'errors' es un diccionario, la clave es el campo donde esta el error y el valor es el mensaje que le pusimos en el serlizador.
        #     return Response(test_user.errors, status=status.HTTP_400_BAD_REQUEST)
            
        users = User.objects.all().values('id','username','email','password')
        users_serializer = UserListSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        users_serializer = UserSerializer(data=request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            return Response(users_serializer.data, status=status.HTTP_200_OK)
        return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
        request=InputSerializer,
    )
@api_view(['GET','PUT','DELETE'])
def user_detail_view(request,pk):
    if request.method == 'GET':
        user = User.objects.filter(id=pk).first()
        if user is not None:
            user_serializer= UserSerializer(user)
            return Response(user_serializer.data)
        else: return Response(f'No se encuentra el usuario con id: {pk}', status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'PUT':
        user = User.objects.filter(id=pk).first()
        #*user es la instancia traida de la db
        user_serializer= UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user = User.objects.filter(id=pk).first()
        if user is not None:
            user.delete()
            return Response({'message':'Usuario eliminado.'}, status=status.HTTP_200_OK)
        else: return Response({'error':'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)
        
