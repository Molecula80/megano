from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin


class ModelListApi(PermissionRequiredMixin, ListModelMixin, CreateModelMixin, GenericAPIView):
    """ Представление для получения списка моделей и создания новой модели. """

    def get(self, request) -> list:
        """
        Метод для получения списка моделей.
        :param request:
        :return: список моделей
        :rtype: list
        """
        return self.list(request)

    def post(self, request, format=None):
        """ Метод для создания новой модели. """
        return self.create(request)


class ModelDetailApi(PermissionRequiredMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """ Представление для получения детальной информации о модели, а также ее редактирования и удаления. """

    def get(self, request, *args, **kwargs):
        """ Метод для получения детальной информации о модели. """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """ Метод для редактирования модели. """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """ Метод для удаления модели. """
        return self.destroy(request, *args, **kwargs)
