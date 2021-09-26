from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.conf import settings



class Role(models.Model):
  '''
  The Role entries are managed by the system,
  automatically created via a Django data migration.
  '''
  HEAD_OF_DEPARTMENT_OFFICER = 1
  COUNTY_SECURITY_OFFICER=2
  REGIONAL_SECURITY_OFFICER = 3
  MINISTER_OF_SECURITY = 4
  ADMIN = 5
  ROLE_CHOICES = (
      (HEAD_OF_DEPARTMENT_OFFICER, 'head_of_department_officer'),
      (COUNTY_SECURITY_OFFICER, 'county_security_officer'),
      (REGIONAL_SECURITY_OFFICER, 'regional_security_officer'),
      (MINISTER_OF_SECURITY, 'minister_of_security'),
      (ADMIN, 'admin'),
  )

  id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

  def __str__(self):
      return self.get_id_display()


class User(AbstractUser):
      roles = models.ManyToManyField(Role)

class Subjects(models.Model):
    fname=models.CharField(max_length=100)
    middle_name=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    birth_certificate_number=models.CharField(max_length=100,unique=True)
    id_no=models.CharField(max_length=100,primary_key=True,unique=True)
    phone=models.CharField(max_length=15,unique=True)
    image=models.FileField(upload_to='uploads/users/firgerprints/',default='uploads/users/default.jpg')
    fingerprint_image=models.FileField(upload_to='uploads/users/firgerprints/')

    def __str__(self):
        return self.fname

    class Meta:
        verbose_name_plural='Subjects'     


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    image=models.ImageField(upload_to='uploads/users/%Y%m%d/',default='uploads/users/default.jpg')
    email = models.EmailField(max_length=100)
    website=models.URLField(max_length=255,null=True,blank=True)
    biography=models.TextField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

