from django.urls import path, include
from rest_framework.routers import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

messages_router = routers.NestedDefaultRouter(router, r'messages', lookup='message')
messages_router.register(r'comments', MessageViewSet, basename='message-comments')

convo_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [] + router.urls