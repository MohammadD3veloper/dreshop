from rest_framework import serializers
from .models import Payment



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'amount',
            'description',
            'mobile',
            'email',
            'authority',
            'ref_id',
            'card_pan',
            'card_hash',
        ]
