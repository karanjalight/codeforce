from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm
from .models import CustomUser

class CustomAdminUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomAdminUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

# class NewUserForm(UserCreationForm):
# 	email = forms.EmailField(required=True)

# 	class Meta:
# 		model = CustomUser
# 		fields = ( "username", "email", "password1", "password2")

# 	# def save(self, commit=True):
# 	# 	user = super(NewUserForm, self).save(commit=False)
# 	# 	user.email = self.cleaned_data['email']
# 	# 	if commit:
# 	# 		user.save()
# 	# 	return user
      
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = CustomUser
		fields = ( "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.is_customer = True
		if commit:
			user.save()
		return user
      
    
