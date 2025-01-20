from rest_framework import serializers  # type: ignore
from .models import Person, Color
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username already exists")
        if data['email']:
            if User.objects.filter(username=data['email']).exists():
                raise serializers.ValidationError("Email already exists")
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data)
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ColorSerializer(serializers.ModelSerializer):  # Updated to ModelSerializer
    class Meta:
        model = Color
        fields = ('id', 'color_name')  # Included 'id' for better referencing

class PeopleSerializer(serializers.ModelSerializer):
    color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all())  # Handles color relationships using IDs
    color_info = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = "__all__"

    def get_color_info(self, obj):
        # Safely check if the color is not None
        if obj.color:
            return {'color_name': obj.color.color_name, 'hex_code': '#000'}
        return None  # Ensure no error if color is None

    def validate(self, data):
        special_characters = "!@£$%\_<>-()=+~[]^?/"
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError("Name cannot contain Special Characters")

        if data['age'] < 18:
            raise serializers.ValidationError("Age should be greater than 18!")

        return data
