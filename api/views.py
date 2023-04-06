
import requests
from django.forms import model_to_dict
from django.contrib.auth.models import User
from users.models import UserProfile
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework import status
from core.models import Illusion, UserResponse
from .serializers import IllusionSerializer, UserSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
from django.utils import timezone

from users.signals import create_user_profile
from recyclebin.models import RecycleBin


# Create your views here.

class IllusionList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = (FileUploadParser,)

    def get(self, request, **kwargs):
        try:
            # logger_request(request, 200)
            result = Illusion.objects.all()
            serializer = IllusionSerializer(result, many=True)
            response_data = {
                "success": 1,
                "data": serializer.data
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)

        except TypeError:
            response_data = {
                "success": 0,
                "data": "Invalid params sent"
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def post(self, request, **kwargs):
        # logger_request(request, 200)
        data = request.data
        print(data)
        keys = data.keys()
        if 'title' not in keys:
            return JsonResponse("Param 'title' is required!", status=status.HTTP_400_BAD_REQUEST, safe=False)

        elif 'portrait_link' not in keys:
            return JsonResponse("Param 'portrait_link' is required!", status=status.HTTP_400_BAD_REQUEST, safe=False)

        elif 'landscape_link' not in keys:
            return JsonResponse("Param 'landscape_link' is required!", status=status.HTTP_400_BAD_REQUEST, safe=False)

        if data['title'] == '' or data['portrait_link'] == '' or data['landscape_link'] == '':
            return JsonResponse('title/portrait_link/landscape_link param cannot be empty ',
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False)
        serializer = IllusionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "success": 1,
                "data": serializer.data
            }

            # -------------------------------------------------------------------------------
            # u = User.objects.create(username=generate_username())
            # u = UserProfile.objects.create(unique_id=data.get('user_name'))
            # print(u.unique_id)
            # print("uuuuuuuuu", u)
            #
            # create_user_profile.send(sender=None, instance=u, action='create_profile', unique_user_id=data['unique_id'])
            # illusion_id = serializer.data['id']
            # user_resp = UserResponse.objects.create(user_id=u.id, illusion_id=illusion_id, success=True)
            # --------------------------------------------------------------------------------

            return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)
        else:
            response_data = {
                "success": 0,
                "data": serializer.errors
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def put(self, request, pk):
        data = request.data

        illusion_obj = Illusion.objects.filter(pk=pk)
        if illusion_obj.exists():
            serializer = IllusionSerializer(Illusion.objects.get(pk=pk), data=data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "success": 1,
                    "data": serializer.data
                }
                return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)
            else:
                response_data = {
                    "success": 0,
                    "data": serializer.errors
                }
                return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            response_data = {
                "success": 0,
                "data": "Record not found"
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def delete(self, request, pk):
        illusion_obj = Illusion.objects.filter(pk=pk)
        if illusion_obj.exists():

            user = request.user
            print("uuu", user)
            user_name = None
            if user and isinstance(user, User):
                user_name = user.username
            illusion = illusion_obj.first()
            print("ill", illusion)
            illusion_dict = model_to_dict(illusion)
            illusion_dict['created_at'] = illusion.created_at.strftime("%Y-%m-%d %H:%M:%S")
            illusion_dict['updated_at'] = illusion.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            recycle_bin = RecycleBin.objects.create(
                db_id=illusion.id,
                table_id='logger',
                data=illusion_dict,
                deleted_by=user_name,
                deleted_at=timezone.now()
            )

            illusion_obj.delete()
            response_data = {
                "success": 1,
                "data": "Record deleted"
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)
        else:
            response_data = {
                "success": 0,
                "data": "Record not found"
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST, safe=False)


class UserList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = (FileUploadParser,)

    def get(self, request, **kwargs):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            response_data = {
                "success": 1,
                "data": serializer.data
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)

        except TypeError:
            response_data = {
                "success": 0,
                "data": "Invalid params sent"
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def post(self, request, **kwargs):

        print(kwargs)
        try:
            data = request.data
            print('d111', data)
            keys = data.keys()
            print("data", data)
            username = data['username']
            if User.objects.filter(username__iexact=username).exists():
                return JsonResponse({"success": 0, "message": "Param '" + username + "' already exists!"},
                                    status=status.HTTP_400_BAD_REQUEST, safe=False)

            unique_id = data['unique_id']
            if UserProfile.objects.filter(unique_id__iexact=unique_id).exists():
                return JsonResponse({"success": 0, "message": f"Param '{unique_id}' already exists!"},
                                    status=status.HTTP_400_BAD_REQUEST, safe=False)

            if 'username' not in keys:
                return JsonResponse("Param 'username' is required!", status=status.HTTP_400_BAD_REQUEST, safe=False)

            elif 'password' not in keys:
                return JsonResponse("Param 'password' is required!", status=status.HTTP_400_BAD_REQUEST, safe=False)

            elif 'unique_id' not in keys:
                return JsonResponse("Param 'unique_id' is required!", status=status.HTTP_400_BAD_REQUEST,
                                    safe=False)

            if data['username'] == '' or data['password'] == '' or data['unique_id'] == '':
                return JsonResponse('username/password/unique_id param cannot be empty ',
                                    status=status.HTTP_400_BAD_REQUEST,
                                    safe=False)
            print('d2222', data)
            # user_resp = post_user(data)
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "success": 1,
                    "data": serializer.data
                }
                print("3333", serializer.data['id'])

                # -------------------------------------------------------------------------------
                create_user_profile.send(sender=None, instance=serializer.data['id'],
                                         action='create_uniqueid_and_image',
                                         unique_user_id=data['unique_id'], image=data.get('image', None))
                # --------------------------------------------------------------------------------

                return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)
            else:
                response_data = {
                    "success": 0,
                    "data": serializer.errors
                }
                return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST, safe=False)

        except TypeError:
            return JsonResponse('Invalid params sent', status=status.HTTP_400_BAD_REQUEST, safe=False)


class UserDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = (FileUploadParser,)

    def get(self, request, **kwargs):
        print(kwargs)
        try:
            user = User.objects.get(pk=kwargs.get('pk'))
            print("uu", user)
            serializer = UserSerializer(user)
            response_data = {
                "success": 1,
                "data": serializer.data
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)

        except TypeError:
            return JsonResponse('Invalid params sent', status=status.HTTP_400_BAD_REQUEST, safe=False)
        except User.DoesNotExist as e:
            response_data = {
                "success": 0,
                "message": str(e),
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST, safe=False)
