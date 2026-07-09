# whatsthedeal_app/context_processors.py

def comment_notifications(request):
    # Fetch the notifications from the session if they exist
    notifications = request.session.get('new_comment_notifications', [])
    
    return {
        'navbar_notifications': notifications,
        'notification_count': len(notifications)
    }