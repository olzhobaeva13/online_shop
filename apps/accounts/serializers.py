from rest_framework import exceptions, serializers

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_password(self, value):
        if len(value) < 5:
            raise exceptions.ValidationError('Password is too short')
        elif len(value) > 20:
            raise exceptions.ValidationError('Password is too long')
        return value
