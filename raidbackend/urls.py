from django.contrib import admin
from django.urls import path
from raidauth.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('users/', UsersAPI.as_view()),
    path('verify-OTP/', VerifyOTP.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('change-status/', ChangeStatus.as_view()),
    path('vehicle-types/', VehicleTypeAPI.as_view()),
    path('upload-documents/', DriverDocumentsAPI.as_view()),
    path('admin/', admin.site.urls),
    path('get-drivers/', GetDriversAPI.as_view()),
    path('ride-history/', RideHistoryAPI.as_view()),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
