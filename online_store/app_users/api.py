from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from .models import User
from .serializers import UserSerializer


class UserListApi(PermissionRequiredMixin, ListModelMixin, CreateModelMixin, GenericAPIView):
    """ Представление для получения списка пользователей и создания нового пользователя. """
    permission_required = ('app_catalog.view_user', 'app_catalog.add_user')
    queryset = User.objects.prefetch_related('groups').all()
    serializer_class = UserSerializer
    filterset_fields = ['is_superuser', 'full_name', 'email', 'is_staff', 'is_active']

    def get(self, request) -> list:
        """
        Метод для получения списка пользователей.
        :param request:
        :return: список пользователей
        :rtype: list
        """
        return self.list(request)

    def post(self, request, format=None):
        """ Метод для создания нового пользователя. """
        return self.create(request)


class UserDetailApi(PermissionRequiredMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """ Представление для получения детальной информации о пользователе, а также его редактирования и удаления. """
    permission_required = ('app_catalog.view_user', 'app_catalog.change_user', 'app_catalog.delete_user')
    queryset = User.objects.prefetch_related('groups').all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """ Метод для получения детальной информации о пользователе. """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """ Метод для редактирования пользователя. """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """ Метод для удаления пользователя. """
        return self.destroy(request, *args, **kwargs)
