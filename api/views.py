
from .models import Profile, User, ChatMessage
from .serializer import MyTokenObtainPairSerializer, RegisterSerializer, MessageSerializer, ProfileSerializer

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.db.models import Subquery, OuterRef, Q
import json


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        messages = ChatMessage.objects.filter(
            id__in=User.objects.exclude(id=user_id).order_by("-id").annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef("id"), receiver=user_id) |
                        Q(receiver=OuterRef("id"), sender=user_id)
                    ).order_by("-date")[:1].values_list("id")
                )
            ).values_list("last_msg")
        ).order_by("-date")
        return messages


class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        sender_id = self.kwargs["sender_id"]
        receiver_id = self.kwargs["receiver_id"]
        messages = ChatMessage.objects.filter(
            sender__in=[sender_id, receiver_id],
            receiver__in=[sender_id, receiver_id],
        )
        return messages


class SendMessage(generics.CreateAPIView):
    serializer_class = MessageSerializer


class ProfileDetails(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]


class SearchUser(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        logged_in_user = self.request.user
        users = Profile.objects.filter(
            Q(user__username__icontains=username) |
            Q(full_name__icontains=username) |
            Q(user__email__icontains=username)
            # & ~Q(user=logged_in_user) # TODO add while using from UI
        )

        if not users.exists():
            return Response({"Details": "No User found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
