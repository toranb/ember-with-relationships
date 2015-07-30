from api.models import Session, Speaker
from rest_framework import serializers

class SpeakerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=False)

    class Meta:
        model = Speaker
        fields = ('id', 'name', )

class SessionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=False)
    speakers = SpeakerSerializer(many=True)

    class Meta:
        model = Session
        fields = ('id', 'name', 'speakers', )

    def update(self, instance, validated_data):
        speakers = validated_data.pop('speakers')
        if instance.speakers.count() == 0 and len(speakers) > 0:
            for s in speakers:
                speaker = Speaker.objects.create(**s)
                instance.speakers.add(speaker)
        return super(SessionSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        speakers = validated_data.pop('speakers')
        session = Session.objects.create(**validated_data)
        for s in speakers:
            speaker = Speaker.objects.create(**s)
            session.speakers.add(speaker)
        return session
