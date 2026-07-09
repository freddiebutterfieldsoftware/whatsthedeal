# whatsthedeal_app/adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from .models import Post

class NotificationAccountAdapter(DefaultAccountAdapter):
    def login(self, request, user):
        # 1. Capture the last_login BEFORE it gets overwritten
        previous_login = user.last_login
        
        # 2. Call the parent login (this updates last_login in the DB)
        super().login(request, user)
        
        # 3. Perform your custom check using the old timestamp
        if previous_login:
            self.get_posts_with_new_comments(request, user, previous_login)

    def get_posts_with_new_comments(self, request, user, since_time):
        posts_with_new_comments = Post.objects.filter(
            user=user,
            comments__created_at__gt=since_time
        ).distinct()

        notifications = []
        for post in posts_with_new_comments:
            notifications.append({
                'url': reverse('whatsthedeal:post-view', kwargs={'pk': post.id})
            })

        if notifications:
            request.session['new_comment_notifications'] = notifications