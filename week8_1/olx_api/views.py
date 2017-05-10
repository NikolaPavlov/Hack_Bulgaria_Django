from django.shortcuts import render
from rest_framework import generics
from .serializer import OfferSerializer
from .models import Offer


# Create your views here.
class OfferList(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OfferDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
