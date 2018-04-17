from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MotionReg
from .serializers import MotionregSerializer
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
@api_view(['POST'])
def recording(request):
    print('POST PRINT', request.data)
    serializer = MotionregSerializer(data=request.data)
    if serializer.is_valid():
        print('VALID', serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('BAD', serializer.data)
    print('ERROR', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



