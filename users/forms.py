from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from quizes.models import Question,Option,Quiz
from .models import UserProfile


class VerifyForm(forms.Form):
    # فیلدهای فرم رو اینجا اضافه کن
    code = forms.CharField(min_length=6,max_length=6, label="کد تایید")

class LoginForm(forms.Form):

    username=forms.CharField()
    password=forms.CharField()

class QuizForm(forms.ModelForm):

    class Meta:
        model=Quiz
        fields = ['title', 'time', 'description']

class QuestionForm(forms.ModelForm):

    class Meta:
        model=Question
        fields='__all__'

class OptionForm(forms.ModelForm):

    class Meta:
        model=Option
        fields='__all__'
    
QuestionFormset=inlineformset_factory(
    Quiz,
    Question,
    form= QuestionForm,
    extra=100,
    can_delete=True

)

OptionFormset=inlineformset_factory(
    Question,
    Option,
    form=OptionForm,
    extra=4,
    can_delete=True,
    
)

class CustomUserCreationForm(UserCreationForm):

    STUDENT = 0
    TEACHER = 1
    ROLE = (
        (STUDENT, _("student")),
        (TEACHER, _("teacher")),
    )

    role = forms.ChoiceField(
        label=_("role"),
        choices=ROLE
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit)
        role = self.cleaned_data['role']
        UserProfile.objects.create(user=user, role=role)
        return user
    
class FullProfileForm(forms.ModelForm, SetPasswordMixin):

    username = forms.CharField(label="نام کاربری")
    email = forms.EmailField(label="ایمیل")
    password = forms.CharField(
        label="پسورد جدید",
        required=False,
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="تکرار پسورد جدید",
        required=False,
        widget=forms.PasswordInput
    )

    class Meta:
        model = UserProfile
        exclude = ['user', 'role']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        # فقط اگر یکی از پسوردها پر بود، مقایسه کن
        if password or password2:
            self.validate_passwords()
        try:
            validate_password(password, user=self.user)
        except ValidationError as e:
               
            raise ValidationError(e.messages)

        return cleaned_data

    def save(self, commit=True):
        profile = super().save(commit=False)

        user = self.user
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')

        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        if commit:
            user.save()
            profile.user = user
            profile.save()

        return profile


