from django.http import HttpResponseForbidden
from django.shortcuts import redirect

class RoleRequiredMixin:
    """
    Mixin برای محدود کردن دسترسی بر اساس نقش کاربر
    """
    allowed_roles = []  # لیست نقش‌های مجاز

    def dispatch(self, request, *args, **kwargs):
        
        try:
            user_profile = request.user.user_profile
        except AttributeError:
            return HttpResponseForbidden("پروفایل کاربر یافت نشد.")

        # بررسی نقش کاربر
        if user_profile.role not in self.allowed_roles:
            return HttpResponseForbidden("شما اجازه دسترسی به این صفحه را ندارید.")
            

        return super().dispatch(request, *args, **kwargs)