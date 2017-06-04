from django.contrib.auth.models import User
from ask.models import ProjectCache, Tag

# popular tags
def popular_tags(request):
    tags = ProjectCache.get_popular_tags()

    return {'popular_tags': tags}