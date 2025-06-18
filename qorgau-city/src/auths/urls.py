from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from auths.views import (
    UserViewSet,
    MyObtainTokenPairView,
    UserRegisterView,
    AvatarViewSet,
    UserActivateView,
    ResetPasswordViewSet,
    ForgotPasswordViewSet,
    SendSmsCodeViewSet,
    UserMeViewSet,
    EducationViewSet,
    ExperienceViewSet,
    AchievementViewSet,
    OtherAchievementViewSet,
)

router = DefaultRouter(trailing_slash=True)
router.register('users', UserViewSet, basename='owners')
router.register('user', UserMeViewSet, basename='user_me')
router.register('user/avatar', AvatarViewSet, basename='user_avatar')
router.register(r'provider_profile/education', EducationViewSet, basename='education')
router.register(r'provider_profile/experience', ExperienceViewSet, basename='experience')
router.register(r'provider_profile/achievement', AchievementViewSet, basename='achievement')
router.register(r'provider_profile/other_achievement', OtherAchievementViewSet, basename='other_achievement')
# router.register(r'education', EducationViewSet, basename='education')
# router.register(r'experience', ExperienceViewSet, basename='experience')
# router.register(r'achievements', AchievementViewSet, basename='achievement')
# router.register(r'other-achievements', OtherAchievementViewSet, basename='other-achievement')

urlpatterns = [
    path('', include(router.urls)),

    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterView.as_view(), name='auth_register'),
    path('users/activate', UserActivateView.as_view({'get': 'get'}), name='user-activate'),
    path('users/resend-activate', UserActivateView.as_view({'get': 'resend'}), name='resend-activate'),
    path('users/reset-password', ResetPasswordViewSet.as_view({'post': 'reset_password'}), name='reset-password'),
    path('users/forgot-password', ForgotPasswordViewSet.as_view({'post': 'forgot_password'}), name='forgot-password'),
    path('users/send-sms-code', SendSmsCodeViewSet.as_view({'post': 'send_sms_code'}), name='send-sms-code'),
    path('users/verify-sms-code', SendSmsCodeViewSet.as_view({'post': 'verify_sms_code'}), name='verify-sms-code'),
]
