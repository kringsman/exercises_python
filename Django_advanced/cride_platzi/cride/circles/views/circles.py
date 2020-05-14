"""Circle views."""

# Django REST Framewrok
from rest_framework import mixins, viewsets

# Permissions 
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.circles import IsCircleAdmin

# serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle, Membership


class CircleViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Circle view set. """

    serializer_class = CircleModelSerializer
    
    def get_queryset(self):
        """Restrict list to public-only"""
        
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def get_permission(self):
        """assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions ]
    
    def perfom_create(self, serializer):
        """"Asign circle admin"""
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )