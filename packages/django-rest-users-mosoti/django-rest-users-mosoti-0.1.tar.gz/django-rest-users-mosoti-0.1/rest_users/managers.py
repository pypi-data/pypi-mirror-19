
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        #do validations
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        
       
        first_name=extra_fields.get('first_name')
        last_name=extra_fields.get('last_name')
        user = self.model(email=email, first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.is_active=True
        user.save(using=self._db)
        return user

    def create_user(self, email,password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,password,**extra_fields)
        
    def create_superuser(self, email,password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email,password, **extra_fields)
        
        

