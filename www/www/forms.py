from django import forms
from .models import Transactions

class CreateOrder(forms.ModelForm):
	class Meta:
		model = Transactions
		fields = ('email','first_name','last_name','address','city','state','pincode','company','GST','phone_number',)
