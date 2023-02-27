from common.api import ModelDetailApi, ModelListApi

from .models import User
from .serializers import UserSerializer


class UserListApi(ModelListApi):
    """ Представление для получения списка пользователей и создания нового пользователя. """
    permission_required = ('app_catalog.view_user', 'app_catalog.add_user')
    queryset = User.objects.prefetch_related('groups').all()
    serializer_class = UserSerializer
    filterset_fields = ['is_superuser', 'full_name', 'email', 'is_staff', 'is_active']


class UserDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о пользователе, а также его редактирования и удаления. """
    permission_required = ('app_catalog.view_user', 'app_catalog.change_user', 'app_catalog.delete_user')
    queryset = User.objects.prefetch_related('groups').all()
    serializer_class = UserSerializer
