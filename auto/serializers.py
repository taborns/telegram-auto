from rest_framework import serializers
from auto import models


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Action
        fields = 'label',
 
class RunningTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RunningTask
        fields = 'task',

    def to_representation(self, data):
        return data.task.entity_ident

class PackageSerializer(serializers.ModelSerializer):
    action = ActionSerializer()
    class Meta:
        model = models.TaskPackage
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    address = serializers.CharField(read_only=True)
    action = ActionSerializer(read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.Task
        exclude = ('random_token',)
        extra_kwargs = {
            'package': {'write_only': True},
        }
        read_only_fields = ('status','target_member_count')
