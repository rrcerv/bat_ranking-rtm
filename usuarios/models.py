from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
import uuid

# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)

# CLASSE PERSONALIZADA DE USUÁRIO. LEMBRE-SE DE COLOCAR O PARÂMETRO AUTH_USER_MODEL NO SETTINGS
class User(AbstractBaseUser, PermissionsMixin):
    Gerente = 'Gerente'
    Vendedor = 'Vendedor'
    GRM = "GRM"
    GTV = "GTV"

    ROLES_CHOICES = (
        (Vendedor, 'Vendedor'),
        (Gerente, 'Gerente'),
        (GRM, "GRM"),
        (GTV, "GTV")
    )

    SUL = 'SUL'
    SPR = 'SPR'
    SPC = 'SPC'
    RIO = 'RIO'
    CTO = 'CTO'
    NNE = 'NNE'

    REGIONAIS_CHOICES = (
        (SUL, 'SUL'),
        (SPR, 'SPR'),
        (SPC, 'SPC'),
        (RIO, 'RIO'),
        (CTO, 'CTO'),
        (NNE, 'NNE')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(blank=True, null=True)
    matricula = models.CharField(max_length=50, null=False, blank=False, unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, default=Vendedor)

    regional = models.CharField(max_length=5, choices=REGIONAIS_CHOICES, default=SUL)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(null=True, max_length=50, blank= True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'matricula'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']