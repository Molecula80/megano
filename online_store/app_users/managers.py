from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """ Менеджер модели пользователя. """
    def create_user(self, email: str, full_name: str, password: str, **extra_fields):
        """
        Метод для создания пользователя.
        :param email:
        :param full_name:
        :param password:
        :param extra_fields:
        :return: модель пользователя
        :rtype: 'User'
        """
        if not email:
            raise ValueError('Укажите адрес эдектронной почты')
        elif not full_name:
            raise ValueError('Укажите фамилию имя и отчество')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, full_name: str, password: str, **extra_fields):
        """ Метод для создания суперпользователя. """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('У суперпользователя должно быть is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('У суперпользователя должно быть is_superuser=True.')
        return self.create_user(email, full_name, password, **extra_fields)
