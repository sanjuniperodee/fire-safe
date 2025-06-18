from rest_framework import serializers
from auths.models import (
    Education,
    Experience,
    Achievement,
    OtherAchievement
)


class EducationSerializer(serializers.ModelSerializer):
    show_photo_to_clients = serializers.BooleanField(default=False)
    performing_now = serializers.BooleanField(default=False)

    class Meta:
        model = Education
        fields = (
            'id',
            'college_name',
            'degree',
            'year_start',
            'year_end',
            'media',
            'show_photo_to_clients',
            'performing_now'
        )

    def validate(self, data):
        if 'year_end' in data and data['year_end'] and not data.get('media') and not self.instance:
            raise serializers.ValidationError(
                "If year_end is provided, diploma image/file must also be included while creating.")

        if self.instance:
            if 'year_end' in data and data['year_end']:
                if not self.instance.media and 'media' not in data:
                    raise serializers.ValidationError(
                        f"If year_end is provided, diploma image/file must also be included while updating.")
            elif 'media' in data and data['media']:
                if not self.instance.year_end and 'year_end' not in data:
                    raise serializers.ValidationError(
                        "If diploma image/file is provided, year_end must also be included while updating.")

        if data.get('performing_now'):
            data['year_end'] = None
            data['media'] = None

        return data

    def update(self, instance, validated_data):
        if validated_data.get('performing_now'):
            instance.year_end = None
            instance.media.delete(save=False)
            instance.media = None
        return super().update(instance, validated_data)


class ExperienceSerializer(serializers.ModelSerializer):
    performing_now = serializers.BooleanField(default=False)

    class Meta:
        model = Experience
        fields = (
            'id',
            'company_name',
            'year_start',
            'year_end',
            'media',
            'performing_now'
        )

    def validate(self, data):
        if 'year_end' in data and data['year_end'] and not data.get('media') and not self.instance:
            raise serializers.ValidationError(
                "If year_end is provided, experience document/image must also be included while creating.")

        if self.instance:
            if 'year_end' in data and data['year_end']:
                if not self.instance.media and 'media' not in data:
                    raise serializers.ValidationError(
                        f"If year_end is provided, experience document/image must also be included while updating.")
            elif 'media' in data and data['media']:
                if not self.instance.year_end and 'year_end' not in data:
                    raise serializers.ValidationError(
                        "If experience document/image is provided, year_end must also be included while updating.")

        if data.get('performing_now'):
            data['year_end'] = None
            data['media'] = None

        return data

    def update(self, instance, validated_data):
        if validated_data.get('performing_now'):
            instance.year_end = None
            instance.media.delete(save=False)
            instance.media = None
        return super().update(instance, validated_data)


class AchievementSerializer(serializers.ModelSerializer):
    show_photo_to_clients = serializers.BooleanField(default=False)

    class Meta:
        model = Achievement
        fields = (
            'id',
            'certificate_name',
            'year_received',
            'media',
            'show_photo_to_clients'
        )


class OtherAchievementSerializer(serializers.ModelSerializer):
    show_photo_to_clients = serializers.BooleanField(default=False)
    performing_now = serializers.BooleanField(default=False)

    class Meta:
        model = OtherAchievement
        fields = (
            'id',
            'name',
            'year_start',
            'year_end',
            'media',
            'show_photo_to_clients',
            'performing_now'
        )

    def validate(self, data):
        if 'year_end' in data and data['year_end'] and not data.get('media') and not self.instance:
            raise serializers.ValidationError(
                "If year_end is provided, other_achievement document/image must also be included while creating.")

        if self.instance:
            if 'year_end' in data and data['year_end']:
                if not self.instance.media and 'media' not in data:
                    raise serializers.ValidationError(
                        f"If year_end is provided, other_achievement document/image must also be included while updating.")
            elif 'media' in data and data['media']:
                if not self.instance.year_end and 'year_end' not in data:
                    raise serializers.ValidationError(
                        "If other_achievement document/image is provided, year_end must also be included while updating.")

        if data.get('performing_now'):
            data['year_end'] = None
            data['media'] = None

        return data

    def update(self, instance, validated_data):
        if validated_data.get('performing_now'):
            instance.year_end = None
            instance.media.delete(save=False)
            instance.media = None
        return super().update(instance, validated_data)
