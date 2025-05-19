from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager, OTPManager
#from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    # اطلاعات پایه
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # وضعیت
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # وضعیت تأیید حساب
    # زمان‌بندی
    date_joined = models.DateTimeField(default=timezone.now)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_selected_role = models.CharField(max_length=32, null=True, blank=True)
    # نقش‌ها
    user_type = models.CharField(max_length=10, choices=[('individual', 'individual'), ('organization', 'organization')], default='individual')
         #اخرین نقشی که کاربر انتخاب کرده
    last_role = models.CharField(max_length=10, choices=[('buyer', 'Buyer'), ('supplier', 'Supplier')])
    objects = UserManager() 

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.phone_number
    




# otp code برای احراز هویت دو مرحله‌ای
class OTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    objects = OTPManager()
    
    def is_valid(self):
        return timezone.now() < self.expires_at

    @staticmethod
    def is_valid_for_user(phone_number):
        return OTP.objects.filter(phone_number=phone_number, expires_at__gt=timezone.now()).exists()

    def __str__(self):
        return f"{self.phone_number} - {self.code}"

    class Meta:
        ordering = ['-expires_at']
























# این ساختار فعلا در نظر گرفته میشه ولی پیاده سازی نمیشه چون قرار لاگ گیری فرق کنه
class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255) 
    device = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"
    class Meta:
        verbose_name = "Login History"
        verbose_name_plural = "Login Histories"
        ordering = ['-login_time']

