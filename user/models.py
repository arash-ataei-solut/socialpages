from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .validators import UnicodeUsernameValidator, UnicodePhoneValidator


class ProfileManager(BaseUserManager):
    def create_user(
            self,
            username,
            password=None,
    ):
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            username,
            password=None
    ):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    is_phone = UnicodePhoneValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    picture = models.ImageField(upload_to='profile', blank=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    email = models.EmailField(_('email address'), max_length=255, blank=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True, validators=[is_phone])
    birth_date = models.DateField(_('birth date'), null=True)

    budget = models.DecimalField(max_digits=10, decimal_places=0, default=100)

    is_admin = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = ProfileManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app 'app_label'?"
        return True

    @property
    def is_staff(self):
        "is the user a member of staff?"
        return self.is_admin

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name) or self.username
