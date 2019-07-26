from django.shortcuts import render, get_object_or_404
from rest_framework import generics, views,pagination
from rest_framework.response import Response
from auto import models, serializers
from blockchain.exchangerates import to_btc
from blockchain.v2.receive import receive
from django.urls import reverse
from blockchain.exceptions import APIException
from telethon.sync import TelegramClient
from telethon import functions, types
import asyncio
import urllib

# Create your views here.
XPUB = "xpub6Bn2E5MU9RTax4opmS32FN9gyuUWMqwrPvHkdyTc1ZJForet1D2bLJW5GS1sQZR1jH9XhdyhhaEzyed84MwopJeBSyRWMCcT5kahWyZ6ntz"
API_KEY = "e5e92fb7-ee1d-4bfc-a060-7412f49bf5b1"
SECRET_KEY = "thestrongestpass"
CONFIRMATION_PASSED = 4
api_id = 875323
api_hash = 'af081d62587aed4d253ded7f1a27f623'
URL_HOME = "http://178.128.89.64/callback/"

def getChannelMemberCount(channelUsername):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with TelegramClient('my-sess', api_id, api_hash) as client:
        # Getting information about yourself
        entity = client.get_entity(channelUsername)
        result = client(functions.channels.GetFullChannelRequest(
            channel=entity
        ))
        
        return result.full_chat.participants_count
class RunningTaskView(views.APIView, pagination.LimitOffsetPagination):
    default_limit = 10
    def get(self, request, *args, **kwargs):
        paginator = pagination.LimitOffsetPagination()
        running_tasks = models.RunningTask.objects.all()
        results = self.paginate_queryset(running_tasks, request)
        serializer = serializers.RunningTaskSerializer(results, many=True)
        return Response(serializer.data)

class InvoiceTaskList(views.APIView):
    
    def get(self, request, invoiceID, *args, **kwargs):
        invoice = get_object_or_404(models.Invoice, pk=invoiceID)
        task = invoice.task
        serializer = serializers.TaskSerializer(task)

        return Response(serializer.data)
        
class TelegramChannelInfoUpdateView(views.APIView):
    def get(self, request, *args, **kwargs):
        if request.GET.get('secret') == SECRET_KEY and request.GET.get('username'):
            usernames = request.GET.getlist('username')
            channelCounts = {}
            for username in usernames:
                channelCount = getChannelMemberCount(username)
                task = models.Task.objects.filter(entity_ident=username, status=models.STAT_RUN).first()
                task.member_count=channelCount
                
                if task.member_count >= task.target_member_count:
                    models.RunningTask.objects.filter(task=task).delete()
                    task.status = models.STAT_COMP
                task.save()
                channelCounts[username] =  channelCount

            return Response({"Done" : channelCounts})
    
        return Response("Login failed")

class CallBackView(views.APIView):

    def get(self, request, *args, **kwargs):
        address = request.GET.get('address')
        secret = request.GET.get('secret')
        confirmations = int(request.GET.get('confirmations'))
        tx_hash = request.GET.get('transaction_hash')
        value_satoshi = float(request.GET.get('value')) 
        invoice = get_object_or_404(models.Invoice, pk=request.GET.get('invoiceID'))
        task = invoice.task
        value = value_satoshi/100000000
        
        packageValue = to_btc('USD', task.package.price)
        print (packageValue, value, task.package.price)
        
        if address != task.address:
            return Response('Incorrect Receiving Address', status=400)
        
        if secret != SECRET_KEY:
            return Response('invalid secret', status=400)
        
        if confirmations >= CONFIRMATION_PASSED:
            payment = models.Payment.objects.create(task=task, amount=value)
            totalAcceptedPayment = sum([ payment.amount for payment in task.payments.all()])
            
            if totalAcceptedPayment >= invoice.expected_price:
            
                if task.running_tasks.count() == 0:
                    models.RunningTask.objects.create(task=task)
                    task.status = models.STAT_RUN
                task.save()

            return Response('*ok*')
        else:
            return Response('Waiting for confirmations')
        # should never reach here!
        return Response('something went wrong', status=500)
        
class TaskListCreate(generics.ListCreateAPIView):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    
    def create(self, request, *args, **kwargs):
        return super(TaskListCreate, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        expected_price_btc = to_btc('USD', serializer.validated_data['package'].price)
        channel_count = getChannelMemberCount(serializer.validated_data['entity_ident'])
        callbackURL = URL_HOME
        invoice = models.Invoice.objects.create(expected_price = expected_price_btc)
        callbackParams = {
                            'secret' : SECRET_KEY, 
                            'invoiceID' : invoice.pk}
        callbackURL += '?' + urllib.parse.urlencode(callbackParams)
        recv = receive(XPUB, callbackURL, API_KEY)
        serializer.save(address = recv.address, 
                        invoice = invoice,
                        member_count = channel_count,
                        target_member_count = channel_count + serializer.validated_data['package'].number, 
                        action = serializer.validated_data['package'].action)
        
        
class PackageList(generics.ListAPIView):
    queryset = models.TaskPackage.objects.all()
    serializer_class = serializers.PackageSerializer

    def list(self, request, action=None):
        if action:
            action = get_object_or_404(models.Action, pk=action)
            packages = action.packages
        else:
            packages = models.TaskPackage.objects.all()

        serializer = self.get_serializer( packages, many=True )
        return Response(serializer.data)
        




