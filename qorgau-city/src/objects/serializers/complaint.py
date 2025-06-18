from rest_framework import serializers

import auths
import objects
from auths.models import CustomUser, UserRole
from auths.serializers import UserShortSerializer
#from helpers.chat_api import generate_jwt_token, create_chat_room
from helpers.logger import log_message
from objects.models import Complaint
from helpers.local_chat_api import create_complaint_chat_room


class ComplaintListSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)
    inspector = UserShortSerializer(read_only=True)
    status = serializers.ChoiceField(choices=objects.Status.choices, read_only=True)

    class Meta:
        model = Complaint
        fields = ('id', 'unique_id', 'author', 'inspector', 'status', 'expiration_date', 'archive_date', 'chat_room_id',
                  'created_at',
                  'updated_at')
        read_only_fields = fields


class ComplaintCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        fields = ('id', 'unique_id',
                  'chat_room_id',
                  'created_at', 'updated_at', 'expiration_date',
                  'city', 'district',
                  'inspector',
                  )
        read_only_fields = (
            'id', 'unique_id',
            'created_at', 'updated_at', 'expiration_date', 'archive_date',
            'chat_room_id',
            'inspector'
        )

    def validate_inspector(self, value):
        # if not value.is_inspector:
        #     raise serializers.ValidationError("The assigned user is not an inspector.")

        # Check if the inspector is active
        # if not value.is_active:
        #     raise serializers.ValidationError("The assigned inspector is not active.")

        inspector_role = UserRole.objects.filter(
            user=value,
            role__role=auths.Role.INSPECTOR,
        ).first()
        if not inspector_role or inspector_role.status != auths.Status.ACCEPTED:
            raise serializers.ValidationError("The assigned inspector's role is not accepted.")

        # Check if the inspector has too many open complaints
        # open_complaints = Complaint.objects.filter(
        #     inspector=value,
        #     status=objects.Status.PENDING,
        # ).count()
        # print(f'open_complaints count: {open_complaints}')
        # if open_complaints >= 10:  # You can adjust this threshold
        #     raise serializers.ValidationError("The assigned inspector has too many open complaints.")

        return value

    def validate(self, data):
        user = self.context['request'].user

        city = data.get('city')
        district = data.get('district')

        # Check the number of pending complaints for the current user
        pending_complaints_count = Complaint.objects.filter(
            author=user,
            status=objects.Status.PENDING
        ).count()

        if pending_complaints_count >= 5:
            raise serializers.ValidationError(
                "You have too many pending complaints (more than 5). "
                "Please wait for some of them to be processed before submitting a new one."
            )

        inspectors = CustomUser.objects.filter(
            role__role='INSPECTOR',
            inspector_jurisdiction_city=city,
            inspector_jurisdiction_district=district
        )
        inspector = Complaint.assign_inspector(city, district)

        if inspectors.exists():
            data['inspector'] = self.validate_inspector(inspector)
        else:
            raise serializers.ValidationError(
                "No matching inspector found for the given location."
            )

        # Check if user already has a pending complaint
        # existing_pending_complaint = Complaint.objects.filter(
        #     author=user,
        #     inspector=data['inspector'],
        #     status=objects.Status.PENDING
        # ).exists()
        # if existing_pending_complaint:
        #     raise serializers.ValidationError(
        #         "You already have a pending complaint. Please wait for it to be processed."
        #     )

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = self.context['request'].user
        validated_data['author'] = user
        inspector = validated_data['inspector']
        validated_data['inspector'] = inspector

        # Create the complaint instance first
        complaint = Complaint.objects.create(**validated_data)

        # Create local chat room (no JWT token needed)
        try:
            chat_room_id = create_complaint_chat_room(
                phone_1=request.user.phone,
                phone_2=inspector.phone,
                complaint_id=complaint.id,
            )

            if chat_room_id:
                complaint.chat_room_id = chat_room_id
                complaint.save()
                return complaint
            else:
                # If chat room creation returns None, continue without failing
                return complaint
        except Exception as e:
            print(f'Failed to create chat room: {e}')
            # Don't fail the complaint creation if chat room creation fails
            return complaint


class ComplaintDetailSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)
    inspector = UserShortSerializer(read_only=True)
    status = serializers.ChoiceField(choices=objects.Status.choices)

    class Meta:
        model = Complaint
        fields = ('id', 'unique_id', 'author', 'inspector',
                  'status', 'expiration_date', 'archive_date', 'chat_room_id',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'unique_id', 'author', 'inspector',
                            'created_at', 'updated_at', 'chat_room_id')

class ComplaintAnswerOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['id', 'status']

    def validate(self, data):
        complaint = self.instance
        if complaint.status == objects.Status.ANSWERED or complaint.status == objects.Status.EXPIRED:
            raise serializers.ValidationError(
                {"status": "This complaint has already been marked as answered."}
            )
        if complaint.status != objects.Status.PENDING:
            raise serializers.ValidationError(
                {"status": f"You cannot mark complaints as answered with status {complaint.status}. Because it is expired "
                           f"with status NOT ANSWERED"}
            )
        return data
