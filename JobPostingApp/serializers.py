from rest_framework import serializers
from .models import JobPosting, TechStack


class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ("name",)


class OtherJobPostingsSerializer(serializers.ModelSerializer):
    tech_stack = TechStackSerializer(many=True, read_only=True)

    class Meta:
        model = JobPosting
        fields = ["id", "position", "reward", "tech_stack"]


class JobPostingSerializer(serializers.ModelSerializer):
    tech_stack = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = JobPosting
        fields = "__all__"

    def validate_tech_stack(self, tech_stack_names):
        """기술 스택 유효성 검사."""
        if not isinstance(tech_stack_names, list):
            raise serializers.ValidationError(
                "tech_stack must be a list of tech stack names."
            )

        tech_stacks = []
        for name in tech_stack_names:
            try:
                tech = TechStack.objects.get(name=name)
                tech_stacks.append(tech)
            except TechStack.DoesNotExist:
                raise serializers.ValidationError(
                    f"TechStack with name {name} does not exist."
                )
        return tech_stacks

    def create(self, validated_data):
        tech_stacks = validated_data.pop("tech_stack", [])
        job_posting = JobPosting.objects.create(**validated_data)
        job_posting.tech_stack.add(*tech_stacks)
        job_posting.save()
        return job_posting

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tech_stack"] = [tech.name for tech in instance.tech_stack.all()]
        return data
