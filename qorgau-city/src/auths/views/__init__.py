from .auth import (
    MyObtainTokenPairView,
    UserRegisterView,
    ResetPasswordViewSet,
    ForgotPasswordViewSet,
)
from .user import (
    UserViewSet,
    UserMeViewSet,
    AvatarViewSet,
)
from .service import (
    UserActivateView,
    SendSmsCodeViewSet,
)
from .profile import (
    EducationViewSet,
    ExperienceViewSet,
    AchievementViewSet,
    OtherAchievementViewSet,
)

__all__ = (
    'UserViewSet',
    'UserMeViewSet',
    'AvatarViewSet',

    'MyObtainTokenPairView',
    'UserRegisterView',
    'ResetPasswordViewSet',
    'ForgotPasswordViewSet',

    'UserActivateView',
    'SendSmsCodeViewSet',

    'EducationViewSet',
    'ExperienceViewSet',
    'AchievementViewSet',
    'OtherAchievementViewSet',
)
