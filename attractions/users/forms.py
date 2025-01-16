from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)


class CustomUserChangeForm(UserChangeForm):
    password = None
    date_of_birth = forms.DateField(
        localize=True,
        widget=forms.DateInput(
            format='%Y-%m-%d', attrs={
                'class': 'form-control', 'type': 'date'}),
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'last_name',
            'first_name',
            'date_of_birth',
            'image')
        # widgets = {
        #     'date_of_birth': forms.DateInput(attrs={'type': 'date'})
            
        # }
# Date = forms.DateField(
#         localize=True,
#         widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
#     )