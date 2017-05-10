from rest_framework import serializers
from .models import Category, Offer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Offer
        fields = '__all__'
