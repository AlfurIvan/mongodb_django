from rest_framework import serializers


class RoadmapStepSerializer(serializers.Serializer):
    step = serializers.IntegerField()
    description = serializers.CharField(max_length=255)


class CertificationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    year = serializers.IntegerField()


class ProjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)


class RoadmapSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    job_title = serializers.CharField(max_length=255)
    tech_stack = serializers.ListField(
        child=serializers.CharField(max_length=50)
    )
    duration = serializers.IntegerField(required=False)
    last_updated = serializers.DateTimeField(required=False)
    roadmap_steps = serializers.ListField(
        child=RoadmapStepSerializer(), required=False
    )
    education = serializers.DictField(required=False)
    certifications = serializers.ListField(
        child=CertificationSerializer(), required=False
    )
    projects_completed = serializers.ListField(
        child=ProjectSerializer(), required=False
    )
    years_of_experience = serializers.IntegerField(required=False)
    desired_genre = serializers.CharField(max_length=50, required=False)
    additional_info = serializers.DictField(required=False)
    difficulty = serializers.CharField(max_length=50)
