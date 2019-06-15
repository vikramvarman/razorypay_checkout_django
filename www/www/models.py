from django.conf import settings
from django.db import models
from django.utils import timezone

class Transactions(models.Model):
	Transaction_Status = [('0', 'In Progress'),('1','succcess'),('2','fail')]
	email = models.EmailField(blank=True)
	first_name = models.CharField(max_length=100,blank=True)
	last_name = models.CharField(max_length=100)
	address = models.TextField()
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	pincode = models.IntegerField()
	company = models.CharField(max_length=150,blank=True)
	GST = models.CharField(max_length=100,blank=True)
	phone_number =  models.IntegerField()
	transaction_id = models.AutoField(primary_key=True)
	Order_id = models.CharField(max_length=100,)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(blank=True, null=True)
	total_price = models.IntegerField()
	Status=	models.IntegerField(
        choices=Transaction_Status,
        default='0',
    )

	def update(self):
		self.updated_at = timezone.now()
		self.save()

	def __str__(self):
		return str(self.transaction_id)
