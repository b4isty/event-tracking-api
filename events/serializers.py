from rest_framework import serializers

from .models import Event, Repo, Actor, Type


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()
    repo = RepoSerializer()
    type = TypeSerializer()

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        actor_data = validated_data.pop('actor')
        repo_data = validated_data.pop('repo')
        type_data = validated_data.pop('type')
        event_obj = Event.objects.create(**validated_data)
        actor_obj = Actor.objects.get_or_create(**actor_data)
        repo_obj = Repo.objects.get_or_create(**repo_data)
        type_obj = Type.objects.get_or_create(**type_data)
        event_obj.actor = actor_obj
        event_obj.repo = repo_obj
        event_obj.type = type_obj
        event_obj.save()
        return event_obj
