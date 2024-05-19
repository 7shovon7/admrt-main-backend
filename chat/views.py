from django.contrib.auth import get_user_model
from django.db.models import Q, Max
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Chat, Conversation
from .serializers import ChatSerializer
from .utils import generate_conversation_id
from core.utils import get_profile_image_url


User = get_user_model()


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        partner_id = self.request.GET.get('partner_id')
        if partner_id:
            # Grab the list of messages with that partner only
            conversation_id = generate_conversation_id(user_id, partner_id)
            # TODO: have to add limit as well
            queryset = self.queryset.filter(conversation_id=conversation_id).order_by('-id')
            return queryset
        else:
            return None

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        partner_id = request.GET.get('partner_id')
        if partner_id:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        # Else Grab the whole list of conversations for the user
        conversations = Conversation.objects.filter(
            Q(id__startswith=f"{user_id}-") | Q(id__endswith=f"-{user_id}")
        ).annotate(
            latest_chat=Max('chats__created_at')
        ).order_by('-latest_chat')
        
        formatted_list = {}
        for conv_id in conversations:
            other_user = conv_id.users.exclude(id=user_id).first()
            if other_user:
                unread_count = Chat.objects.filter(conversation=conv_id, sender=other_user, delivered=False).count()
                formatted_list[other_user.id] = {
                    "full_name": other_user.full_name,
                    "profile_image": get_profile_image_url(other_user.profile.profile_image),
                    "unread_messages": unread_count
                }
        return Response(formatted_list)

    def perform_create(self, serializer):
        sender = self.request.user
        receiver_id = self.request.data.get('receiver_id')
        receiver = get_object_or_404(User, id=receiver_id)

        conversation_id = generate_conversation_id(sender.id, receiver.id)

        conversation, created = Conversation.objects.get_or_create(id=conversation_id)
        if created:
            conversation.users.set([sender, receiver])

        serializer.save(sender=self.request.user, conversation=conversation)
