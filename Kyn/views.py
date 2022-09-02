from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer
from main.models import User, UserEvent

@api_view(['GET'])
def eventList(request):
    events = UserEvent.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def eventDetail(request, id):
    try:
        event = UserEvent.objects.get(id=id)
    except UserEvent.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event, many=False)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = EventSerializer(instance=event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response("Event has been successfully deleted!")

@api_view(['POST'])
def eventCreate(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
