from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from raidauth.serializer import *
from .emails import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.db.models import Q
from .custom_permissions import *
from django.http import QueryDict
from django.db.models import F  


class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data = data)
            if serializer.is_valid():

                serializer.save()
                send_otp_email(serializer.data['username'])
                return Response({
                    'status': 200,
                    'message': 'registration successfull',
                    'data': serializer.data,
                })

            return Response({
                'status': 400,
                'message': serializer.errors,
                'data': serializer.errors,
            })

        except Exception as e:
            print(e)


class VerifyOTP(APIView):
    def post(self, request):
        try:
            data= request.data
            serializer = VerifyAccountSerializer(data = data)
            if serializer.is_valid():
                username = serializer.data['username']
                otp = serializer.data['otp']


                user = User.objects.filter(username = username)

                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'Not found',
                        'data': 'User not found',
                    })


                if user[0].otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'Invalid OTP',
                        'data': 'Wrong OTP',
                    })
                    

                user = user.first()
                user.is_verified = True

                if(user.user_type == 'driver'):
                    user.user_type = 'driver'
                    # user = RideHistory.objects.create(user = user)
                    driver_doc = DocumentsList(driver_id = user)
                    driver_doc.save()
                user.save()
                return Response({
                    'status': 200,
                    'message': 'Account verified',
                    'data': 'OTP Verified',
                })

            return Response({
                'status': 400,
                'message': serializer.errors,
                'data': serializer.errors,
            })
        except Exception as e:
            print(e)


class RideHistoryAPI(APIView):
    def get(self, request):
        
        users = User.objects.filter(Q(user_type='user') | Q(user_type='driver'))
        serializer = UserSerializer(users, many = True)

        return {
            'status': 200,
            'data': serializer.data
        }





class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = User.objects.get(username = username, password = password, is_verified=True, is_active = True)
        try:
            if user:
                token, created = Token.objects.get_or_create(user = user)
                response = Response({
                    'status':  200,
                    'token': token.key
                })
                response.set_cookie('auth_token', str(token))
                return response
            return Response({
                'status': 200,
                'message': 'Invalid credentails'
            })
        except Exception as e:
            print(e)
            return({
                'status': 200,
                'message': 'Something went wrong'
            })

class LogoutAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.user.auth_token)
        request.user.auth_token.delete()

        return Response({
            'status': 200,
            'message': 'Loggedout successfully'
        })



class VehicleTypeAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def post(self, request):
        data  = request.data
        vehicle = VehicleTypeSerializer(data = data)
        if vehicle.is_valid():
            vehicle.save()
            print("saved successfully")
            return Response({
                'status': 200,
                'message': 'vehicle saved successfully'
            })
        return Response({
            'status': 500,
            'message': 'unable to save vehicle'
        })

    def get(self, request):
        try:
            vehicles = VehicleType.objects.all()

            payload = []

            for vehicle in vehicles:
                payload.append({
                    'vehicle_name': vehicle.vehicle_name,
                    'cost_per_km': vehicle.cost_per_km,
                    'status': vehicle.status,
                    'vehicle_image': str(vehicle.vehicle_image),
                })


            return Response({
                'status': 200,
                'data': payload
            })

        except Exception as e:
            print(e)


class GetDriversAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        users = User.objects.filter( Q(user_type='driver'))
        serializer = UserSerializer(users, many = True)

        doc_status = DocumentsList.objects.filter(driver_id=request.user.id).distinct('driver_id')
        driver_doc = doc_status.values('status')
        print(driver_doc)



        return Response({
            'status': 200,
            'data': serializer.data
        })




class DriverDocumentsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsDriver]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        documents = DocumentsList.objects.all()
        payload = []

        for document in documents:
            payload.append({
                "links": [
                    {
                    'name': 'aadhar',
                    'link':str(document.aadhar_doc)
                    },
                    {
                      'name': 'pancard',
                    'link':str(document.pancard_doc) 
                    },
                    {
                        'name': 'voter',
                    'link':str(document.voter_doc)
                    },
                    {
                        'name': 'license',
                    'link':str(document.license_doc)
                    },
                    {
                        'name': 'rc',
                    'link':str(document.rc_doc)
                    },
                    {
                        'name': 'insurance',
                    'link':str(document.insurance_doc)
                    },
                ],
              
                'status': str(document.license_doc),
                'driver_id': str(request.user.id),
                'status': str(document.status),
            })

        return Response({
                'status': 200,
                'data': payload
            })

    def put(self, request):
        data  = request.data
        data['driver_id'] = request.user.id
        user = DocumentsList.objects.get(driver_id = request.user.id)
        documents = DriverDocumentsSerializer(user, data = data)
        if documents.is_valid():
            documents.save()
            print("Driver Doc successfully")
            return Response({
                'status': 200,
                'message': 'vehicle saved successfully'
            })
        return Response({
            'status': 500,
            'message': 'unable to save vehicle'
        })



class UsersAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        users = User.objects.filter(Q(user_type='user') | Q(user_type='driver'))
        serializer = UserSerializer(users, many = True)

        return Response({
            'status': 200,
            'data': serializer.data
        })


class ChangeStatus(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]
    def post(self, request):
        data = request.data
        username = data.get('username')
        status = data.get('status')
        user = User.objects.filter(username = username)
        if user:
            user = user.first()
            if(status == 'Active'):
                user.is_active = True
            else:
                user.is_active = False

            user.save()
            return Response({
                    'status': 200,
                    'message': 'Status Changed',
                    'data': 'Status Changed',
                })


