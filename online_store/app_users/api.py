from django.core.exceptions import PermissionDenied

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from .models import User
from .serializers import UserSerializer


class UserListApi(ListModelMixin, CreateModelMixin, GenericAPIView):
    """ Представление для получения списка пользователей и создания нового пользователя. """
    queryset = User.objects.prefetch_related('groups', 'user_permissions').all()
    serializer_class = UserSerializer
    filterset_fields = ['is_superuser', 'full_name', 'email', 'is_staff', 'is_active']

    def get(self, request):
        if not request.user.has_perm('app_users.view_user'):
            raise PermissionDenied()
        return self.list(request)

    def post(self, request, format=None):
        if not request.user.has_perm('app_users.add_user'):
            raise PermissionDenied()
        return self.create(request)


class UserDetailApi(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """ Представление для получения детальной информации о пользователе, а также его редактирования и удаления. """
    queryset = User.objects.prefetch_related('groups', 'user_permissions').all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('app_users.view_user'):
            raise PermissionDenied()
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm('app_users.change_user'):
            raise PermissionDenied()
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm('app_users.delete_user'):
            raise PermissionDenied()
        return self.destroy(request, *args, **kwargs)
