from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import ApplicationSerializer


@api_view(['POST'])
def get_deposite(request):
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        application = serializer.save()
        result = application.calc_deposit()
        return Response(result, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
