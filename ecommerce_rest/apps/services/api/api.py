from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

# @extend_schema(
#         request=InputSerializer,
#     )
@api_view(['GET'])
def services_api_view(request):
    if request.method == 'GET':
        print('hola')
        return Response('holi')