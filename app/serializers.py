from todoapp.models import Todos
from rest_framework import serializers


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True) # data saving worked only when read_only is true ...Why ??? no idea
    # user already created in model
    class Meta:
        model = Todos
        fields = "__all__"

    def create(self, validated_data): # Its for adding context value(passed from view) "user" to serializer
        user = self.context.get("user")
        return Todos.objects.create(**validated_data,user=user) #only validated data
