from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from users.serializers import TokenRefreshSerializer
from users.views import TokenObtainPairPatchedView, CustomTokenRefreshView

from rest_framework_simplejwt import views as jwt_views
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from reviews.views import ProductViewSet, ImageViewSet

# from rest_framework_jwt.settings import api_settings
#
# if api_settings.JWT_AUTH_COOKIE:
#     from rest_framework_jwt.authentication import JSONWebTokenAuthentication
#     from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer
#     from rest_framework_jwt.views import RefreshJSONWebToken
#
#     RefreshJSONWebTokenSerializer._declared_fields.pop('token')
#
#     class RefreshJSONWebTokenSerializerCookieBased(RefreshJSONWebTokenSerializer):
#         def validate(self, attrs):
#             if 'token' not in attrs:
#                 if api_settings.JWT_AUTH_COOKIE:
#                     attrs['token'] = JSONWebTokenAuthentication().get_jwt_value(self.context['request'])
#             return super(RefreshJSONWebTokenSerializerCookieBased, self).validate(attrs)
#
#     RefreshJSONWebToken.serializer_class = RefreshJSONWebTokenSerializerCookieBased
#
######begin
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# router = DefaultRouter()
# router.register(r'product', ProductViewSet, basename='Product')
# router.register(r'image', ImageViewSet, basename='Image')

#####end

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/token', TokenObtainPairPatchedView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


