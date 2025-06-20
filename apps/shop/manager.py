from django.contrib.auth.base_user import BaseUserManager
from asgiref.sync import sync_to_async


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('Telefon raqamini kiriting !')  # noqa

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.update({
            'is_staff': True,
            'is_superuser': True,
        })

        return self.create_user(phone_number, password, **extra_fields)

    @sync_to_async
    def bot_create_user(self, fullname, telegram_id, **extra_fields):
        if self.model.objects.filter(telegram_id=telegram_id).exists():
            return None
        user = self.model(fullname=fullname, telegram_id=telegram_id, **extra_fields)

        """ set_unusable_password foydalanuvchi hech qanday parol bilan login qila olmasligini ta'minlaydi ,
            set_unusable_password() → password maydoniga ! bilan boshlangan random hash yozadi.
        """
        user.set_unusable_password()
        user.save(using=self._db)

        return user
