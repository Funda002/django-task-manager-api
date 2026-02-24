from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    # We can explicitly show who the author is (just their name)
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'author_name']