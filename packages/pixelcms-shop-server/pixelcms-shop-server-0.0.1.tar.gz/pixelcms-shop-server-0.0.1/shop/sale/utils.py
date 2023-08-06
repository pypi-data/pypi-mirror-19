from .models import Cart


def get_cart(request, cart_pk=None):
    if request.user.is_authenticated:
        customer = request.user.customer
        return Cart.objects.filter(customer=customer).first()
    else:
        customer = None
        try:
            return Cart.objects.get(customer=customer, pk=cart_pk)
        except Cart.DoesNotExist:
            return None
