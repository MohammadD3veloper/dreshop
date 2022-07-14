from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PaymentSerializer
from .models import Payment
from zeep.client import Client
import json



MERCHANT_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
CALLBACK_URL = 'http://localhost:8000/verify/'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl/')


# Create your views here.
class PaymentRequest(generics.GenericAPIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(commit=False)
        obj.user = request.user
        obj.save()
        result = client.service.PaymentRequest(
            MERCHANT_ID,
            obj.amount,
            obj.description,
            obj.author.email,
            '09123456789',
            CALLBACK_URL
        )
        if result.Status == 100 or result.Status == 101:
            obj.authority = result.Authority
            obj.save()
            return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
        return Response({
            json.dumps(result)
        })



class PaymentVerify(generics.GenericAPIView): 
    def get(self, request):
        qstatus = request.GET.get('Status')
        authority = request.GET.get('authority')
        if qstatus == "OK":
            payment = Payment.objects.get(authority=authority)
            result = client.service.PaymentVerification(MERCHANT_ID, authority, payment.amount)
            if result.Status == 100 or result.Status == 101:
                payment.ref_id = result.RefID
                payment.save()
                serializer = PaymentSerializer(data=payment)
                return Response({
                    serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'PaymentError': "Transaction failed, or canceled by the user."
            }, status=status.HTTP_403_FORBIDDEN)
        return Response({
            'PaymentError': "Transaction failed, or canceled by the user."
        }, status=status.HTTP_403_FORBIDDEN)
