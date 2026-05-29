from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class UserProfile(models.Model):
    
    user=models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE,related_name='user_profile')
    STUDENT=0
    TEACHER=1
    ROLE=((STUDENT,_("student")),(TEACHER,_('teacher')))
    role=models.IntegerField(_("role"),choices=ROLE,default=0)
    first_name=models.CharField(_('first name'))
    last_name=models.CharField(_('last name'))
    birth_date=models.DateField(_('date of birth'))
    def is_teacher(self):
        return self.role == self.TEACHER
    
    def get_role_display(self):
        return dict(self.ROLE).get(self.role, "Unknown")



