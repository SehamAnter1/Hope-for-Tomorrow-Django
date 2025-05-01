import stripe
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Project
stripe.api_key = settings.STRIPE_SECRET_KEY
print('api_key',settings.STRIPE_SECRET_KEY)
class CreateCheckoutSessionView(APIView):
    def post(self, request):
        try:
            YOUR_DOMAIN = "http://localhost:3000"  
            project_id = request.data.get('projectId')
            price = request.data.get('price')
            project = Project.objects.get(id=project_id)
            project_name = project.title
            project_image_url = project.cover.url
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': project_name,
                                'images':[project_image_url],
                            },
                            'unit_amount': price*100, 
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
