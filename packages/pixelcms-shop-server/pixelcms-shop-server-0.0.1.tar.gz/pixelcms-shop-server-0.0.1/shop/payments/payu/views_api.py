import hashlib
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import settings as payu_settings
from .models import PayuPayment


@api_view(['POST'])
def notify_view(request):
    signature = request.META.get('HTTP_OPENPAYU_SIGNATURE').split(';')
    signature_data = {}
    for param in signature:
        try:
            param = param.split('=')
            signature_data[param[0]] = param[1]
        except IndexError:
            continue

    try:
        incoming_signature = signature_data['signature']
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    second_md5_key = payu_settings.PAYU_SECOND_MD5_KEY.encode('utf-8')
    expected_signature = hashlib.md5(request.body + second_md5_key).hexdigest()
    if incoming_signature != expected_signature:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        data = json.loads(request.body.decode('utf-8'))
        payu_order_id = data['order']['orderId']
        order_id = data['order']['extOrderId']
        payment_status = data['order']['status']
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        payment = PayuPayment.objects.exclude(internal_status='COMPLETED').get(
            payu_order_id=payu_order_id,
            order__order_id=order_id
        )
    except (PayuPayment.DoesNotExist, ValueError):
        return Response(status=status.HTTP_200_OK)

    if status in ('PENDING', 'WAITING_FOR_CONFIRMATION', 'COMPLETED',
                  'CANCELED', 'REJECTED'):
        payment.internal_status = payment_status
        payment.save()
    return Response(status=status.HTTP_200_OK)
