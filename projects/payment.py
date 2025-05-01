import stripe
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

stripe.api_key = settings.STRIPE_SECRET_KEY
print('api_key',settings.STRIPE_SECRET_KEY)
class CreateCheckoutSessionView(APIView):
    def post(self, request):
        try:
            YOUR_DOMAIN = "http://localhost:3000"  
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'T-shirt',
                                'images':['https://res.cloudinary.com/dovnjzpgf/image/upload/v1/media/project_covers/advantimg_ajtbvh'],
                            },
                            'unit_amount': 2000, 
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=f'{YOUR_DOMAIN}/success/',
                cancel_url=f'{YOUR_DOMAIN}/cancel/',
            )

            return Response({
                'id': checkout_session.id
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
