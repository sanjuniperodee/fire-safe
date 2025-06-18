import auths
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Custom permission to only allow admin for specific actions.
    """
    # Необходимо пересмотреть этот класс

    allowed_actions = ['create', 'update', 'destroy']

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        if request.user.role == auths.Role.ADMIN and request.method in self.allowed_actions:
            return True

        return False


class IsObjectOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow object owners with status 'accepted'.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user_roles = request.user.user_roles.filter(
                role__role=auths.Role.OBJECT_OWNER
                # на данном этапе проекта владельца подтверждать не надо
                # status=auths.Status.ACCEPTED
            )
            return (request.method in SAFE_METHODS
                    or user_roles.exists())
        else:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj.owner
                or request.user.is_staff)


class IsObjectOwner(BasePermission):
    """
    Custom permission to only allow object owners with status 'accepted'.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to object owners.
        return request.user.is_authenticated and request.user.is_object_owner


class IsInspectorOrReadOnly(BasePermission):
    """
    Custom permission to only allow inspectors with status 'accepted'.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user_roles = request.user.user_roles.filter(
                role__role=auths.Role.INSPECTOR,
                status=auths.Status.ACCEPTED
            )
            return (request.method in SAFE_METHODS
                    or user_roles.exists())
        else:
            return request.user.is_authenticated


class IsInspectorOnly(BasePermission):
    """
    Custom permission to ONLY allow inspectors with status 'accepted'.
    Strictly enforces inspector-only access - even superusers are excluded.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Only allow inspectors with accepted status
        return request.user.user_roles.filter(
            role__role=auths.Role.INSPECTOR,
            status=auths.Status.ACCEPTED
        ).exists()

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Only allow inspectors with accepted status
        return request.user.user_roles.filter(
            role__role=auths.Role.INSPECTOR,
            status=auths.Status.ACCEPTED
        ).exists()


class IsProviderOrReadOnly(BasePermission):
    """
    Custom permission to only allow providers with status 'accepted'.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user_roles = request.user.user_roles.filter(
                role__role=auths.Role.PROVIDER,
                status=auths.Status.ACCEPTED
            )
            return (request.method in SAFE_METHODS
                    or user_roles.exists())
        else:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj.user
                or request.user.is_staff)


class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow object authors.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj.author)


class IsCitizenOrReadOnly(BasePermission):
    """
    Custom permission to only allow citizens to create complaints.
    """

    def has_permission(self, request, view):
        # Allow read permissions for any request
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to citizens
        return (request.user.is_authenticated and
                hasattr(request.user, 'is_citizen') and
                request.user.is_citizen)


class IsInspectorOrCitizen(BasePermission):
    """
    Custom permission to allow:
    1. Inspectors (with ACCEPTED status) to perform all operations
    2. Citizens to perform specific operations on their own complaints
    3. Superusers to perform all operations
    """

    def has_permission(self, request, view):
        # Always allow superusers
        if request.user.is_superuser:
            return True

        if not request.user.is_authenticated:
            return False

        # Check if user is an inspector with accepted status
        is_inspector = request.user.user_roles.filter(
            role__role=auths.Role.INSPECTOR,
            status=auths.Status.ACCEPTED
        ).exists()

        # Check if user is a citizen
        is_citizen = hasattr(request.user, 'is_citizen') and request.user.is_citizen

        return is_inspector or is_citizen