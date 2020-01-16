from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
import json
import urllib.parse
import urllib.request

BASE_URL='http://cgw01.nlp.nhnsystem.com:8000/api'
@api_view(['GET', 'POST'])
def index(request):
    return Response({"message": "Hello, world!"})

@api_view(['GET', 'POST'])
def category(request):
    if request.method == "POST":
        if len(Category.objects.filter(category=request.data["category"])) == 0:
            serializers = CategorySerializer(data=request.data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()

    categoryset = Category.objects.all().order_by('order')
    serializers = CategorySerializer(categoryset, many=True)
    return Response(serializers.data)

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == "POST":
        print(request.data)
        for category in request.data:
            tc = Category.objects.get(id=category["id"])
            tc.order = category["order"]
            tc.save();

    categoryset = Category.objects.all().order_by('order')
    serializers = CategorySerializer(categoryset, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def delete_category(request, pid):
    category = Category.objects.get(id=pid).category
    for i in Item.objects.filter(category=category):
        i.delete()

    Category.objects.get(id=pid).delete()

    categoryset = Category.objects.all()
    serializers = CategorySerializer(categoryset, many=True)
    return Response(serializers.data)

@api_view(['GET', 'POST'])
def item(request):
    if request.method == "POST":
        category = request.data["category"]
        if len(Item.objects.filter(name=request.data["name"])) == 0:
            serializers = ItemSerializer(data=request.data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()

    if request.method == 'GET':
        category = request.GET.get("category", "")

    itemset = Item.objects.filter(category=category)
    serializers = ItemSerializer(itemset, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def delete_item(request, pid):
    Item.objects.get(id=pid).delete()
    return Response({})

@api_view(['GET'])
def update_count(request, pid, count):
    item = Item.objects.get(id=pid)
    item.count = count
    item.save();
    return Response({})

@api_view(['GET'])
def update_limit(request, pid, count):
    item = Item.objects.get(id=pid)
    item.limit = count
    item.save();
    return Response({})

# Create your views here.
