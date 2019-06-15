from django.http import HttpResponse, HttpResponseRedirect
from .models import Transactions
from .forms import CreateOrder
from django.shortcuts import render, get_object_or_404, redirect
import logging
from django.contrib import messages
import razorpay
from django.conf import settings 




def checkout(request, amount="500", shipping="50" ,total ="550"):
	if request.method == 'GET':
		amount = amount
		Shipping = shipping
		Total = total
		Form = CreateOrder()
		Item = {'name':'Item Name','MRP':amount,'Shipping':Shipping,'Total':Total}
		data = {'form':Form, 'item':Item}
		return render(request, 'www/checkout.html', data)
	try:
		transaction = Transactions()
		RAZOR_KEY=settings.RAZOR_KEY
		RAZOR_SECRET=settings.RAZOR_SECRET
		api_data = {'amount' :total, 'currency' : 'INR', 'receipt' : '001', 'payment_capture' :'1' }
		client = razorpay.Client(auth=(RAZOR_KEY, RAZOR_SECRET))
		new_order = client.order.create(data=api_data)
		form = CreateOrder(request.POST)
		if form.is_valid():
			transaction = form.save(commit=False)
			transaction.Order_id = new_order['id']
			transaction.total_price = total
			transaction.Status = '0'
			transaction.save()
			return redirect('payment', pk=transaction.transaction_id)

	except Exception as e:
		logging.getLogger("error_logger").error("Unable to get orders. "+repr(e))
		messages.error(request,"Unable to get orders. "+repr(e))


def payment(request, pk):
	if request.method == 'GET':
		res = "new page"+pk
		transaction = Transactions.objects.get(pk=pk)
		if transaction.Status != 0 :
			return HttpResponseesponseNotFound("Invalid order") 
		name = transaction.first_name+" "+transaction.last_name
		address = transaction.address
		city = transaction.city
		order_id = transaction.Order_id
		amount = '123456'
		key = 'rzp_test_8jOyhNXakwp6nu'
		email = transaction.email
		phone = transaction.phone_number
		data = {'name' : name, 'address' : address, 'city' : city,
			'order_id' : order_id, 'amount' : amount, 'key' : key, 'email': email}
		return render(request, 'www/payment.html', data)


def summary(request, pk):
	transaction = Transactions.objects.get(pk=pk)
	RAZOR_KEY=settings.RAZOR_KEY
	RAZOR_SECRET=settings.RAZOR_SECRET
	client = razorpay.Client(auth=(RAZOR_KEY, RAZOR_SECRET))
	order_id = transaction.Order_id
	payment_capture = client.order.payments(order_id)
	if payment_capture['items'][0]['captured'] == True:
		transaction.Status='1'
		transaction.update()
		return HttpResponse('success')
	else :
		transaction.Status='2'
		transaction.update()
		return HttpResponse('failed')