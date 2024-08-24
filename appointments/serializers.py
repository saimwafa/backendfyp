from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import User, Doctor, Review, Appointment

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'phone', 'nic_number', 'password', 'location']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            nic_number=validated_data['nic_number'],
            password=validated_data['password'],
            location=validated_data.get('location')
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.nic_number = validated_data.get('nic_number', instance.nic_number)
        instance.location = validated_data.get('location', instance.location)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'email', 'phone', 'name', 'speciality', 'nic_number', 'location']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user.is_doctor = True
        user.save()
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.name = validated_data.get('name', instance.name)
        instance.speciality = validated_data.get('speciality', instance.speciality)
        instance.nic_number = validated_data.get('nic_number', instance.nic_number)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=[('doctor', 'Doctor'), ('user', 'User')])
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        role = data.get('role')
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if (role == 'doctor' and user.is_doctor) or (role == 'user' and not user.is_doctor):
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid role for the given credentials")
        else:
            raise serializers.ValidationError("Invalid credentials")

        return data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'doctor', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['doctor', 'user']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'user', 'date', 'time', 'status']
        read_only_fields = ['status']
