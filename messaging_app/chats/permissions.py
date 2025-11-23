from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Conversation


class IsParticipantOfConversation(BasePermission):
    
    # Allows access only to participants of a conversation.

    def has_object_permission(self, request, view, obj):
        # If the object is a Message → check obj.conversation
        if hasattr(obj, "conversation"):
            conversation = obj.conversation
        else:
            # If object is a Conversation
            conversation = obj

        return request.user in conversation.participants.all()
