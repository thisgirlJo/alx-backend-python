from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
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
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, min_length=8)
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords do not match")
        return data
    

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender', 
            'message_body', 
            'sent_at']
        
        def create(self, validated_data):
            return Message.objects.create(**validated_data)
    
class ConversationSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants', 
            'created_at']
    def create(self, validated_data):
        return Conversation.objects.create(**validated_data)