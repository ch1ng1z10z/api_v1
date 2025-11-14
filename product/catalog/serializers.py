from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Category, Product, Review, UserConfirmation



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название категории должно быть минимум 2 символа.")
        return value



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Название продукта должно быть минимум 3 символа.")
        return value

    def validate_description(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Описание должно быть минимум 10 символов.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0.")
        return value

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Категория не существует.")
        return value


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

    def validate_text(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Текст отзыва должен быть минимум 5 символов.")
        return value

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value

    def validate_product(self, value):
        if not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Продукт не найден.")
        return value


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        user.is_active = False
        user.save()

        UserConfirmation.objects.create(user=user)

        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Неверный логин или пароль.")

        if not user.is_active:
            raise serializers.ValidationError("Аккаунт не подтверждён.")

        data['user'] = user
        return data



class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        username = data['username']
        code = data['code']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")

        try:
            confirm = user.confirmation
        except UserConfirmation.DoesNotExist:
            raise serializers.ValidationError("Код подтверждения отсутствует.")

        if confirm.code != code:
            raise serializers.ValidationError("Код неверный.")

        data['user'] = user
        return data

    def save(self, validated_data):
        user = validated_data['user']
        user.is_active = True
        user.save()

        user.confirmation.delete()

        return user
