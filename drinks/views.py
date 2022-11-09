from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def drink_list(request):

    if request.method == 'GET':
        drinks = Drink.objects.all()
        serialized_drinks = DrinkSerializer(drinks, many=True)
        return JsonResponse({'drinks': serialized_drinks.data})

    if request.method == 'POST':
        serialized_drinks = DrinkSerializer(data=request.data)
        if serialized_drinks.is_valid():
            serialized_drinks.save()
            return Response(serialized_drinks.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, id):

    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serialized_drink = DrinkSerializer(drink)

        return Response(serialized_drink.data)

    elif request.method == 'PUT':
        new_serialized_drink = DrinkSerializer(drink, data=request.data)

        if new_serialized_drink.is_valid():
            new_serialized_drink.save()
            return Response(new_serialized_drink.data)

        return Response(new_serialized_drink.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
