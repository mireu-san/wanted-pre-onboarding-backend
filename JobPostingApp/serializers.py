from rest_framework import serializers
from .models import JobPosting


class OtherJobPostingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ["id", "position", "reward", "tech_stack"]


class JobPostingSerializer(serializers.ModelSerializer):
    other_job_postings = serializers.SerializerMethodField()

    class Meta:
        model = JobPosting
        fields = "__all__"

    def get_other_job_postings(self, obj):
        # 현재 채용공고와 동일한 회사의 다른 채용공고를 조회
        other_postings = JobPosting.objects.filter(company=obj.company).exclude(
            id=obj.id
        )
        return OtherJobPostingsSerializer(other_postings, many=True).data

    def validate_reward(self, value):
        """Validate the reward amount."""
        if value < 0:
            raise serializers.ValidationError("Reward must be non-negative.")
        return value
