from rest_framework import serializers
from .models import JobPosting


class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = "__all__"

    def validate_reward(self, value):
        """Validate the reward amount."""
        if value < 0:
            raise serializers.ValidationError("Reward must be non-negative.")
        return value
