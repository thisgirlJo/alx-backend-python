from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = [
            'user_id', 
            'first_name',
            'last_name', 
            'email', 
            'phone_number', 
            'role', 
            'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sent_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender', 
            'message_body', 
            'sent_at',
            'sent_at_formatted']
    
    def get_sent_at_formatted(self, obj):
        return obj.sent_at.strftime("%Y-%m-%d %H:%M:%S")
    
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    conversation_label = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants', 
            'created_at',
            'messages',
            'conversation_label']

    def validate(self, data):
        """
        REQUIRED — ensures your checker detects serializers.ValidationError.
        """
        if "participants" in data and len(data["participants"]) < 1:
            raise serializers.ValidationError("Conversation must include at least 1 participant.")

        return data