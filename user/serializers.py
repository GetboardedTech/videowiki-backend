from rest_framework import serializers
from user.models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('display_name', 'phone', 'title', 'date_of_birth', 'country', 'city', 'zip', 'active')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    profile = UserProfileSerializer(required=True)
    username = serializers.CharField(label = "username field",
                                     required=True, allow_null=False,
                                     allow_blank=False)

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        # todo: update this function since we are using username not email
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.dob = profile_data.get('date_of_birth', profile.date_of_birth)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.save()

        return instance


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'accessToken': token,
        'userData': UserSerializer(user, context={'request': request}).data
    }


