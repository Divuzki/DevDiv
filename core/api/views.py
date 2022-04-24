from django.db.models import Q
from django.conf import settings
from .permissions import IsOwnerOrReadOnly
from users.models import Post
from .serializers import PostSerializer

# Third Party
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from taggit.models import Tag


User = settings.AUTH_USER_MODEL


# Post Class Based View
class PostCreateAPI(generics.CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostListAPI(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = Post.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(author__username__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(hashtag__name__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        return qs

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class PostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


@api_view(['GET', ])
def api_latest_post_view(request, *args, **kwargs):
    data = {}
    # Tech
    tech = Post.objects.filter(
        category__iexact="technology").order_by('-date_posted').first()
    tech = PostSerializer(tech).data

    # News
    news = Post.objects.filter(
        category__iexact="local").order_by('-date_posted').first()
    news = PostSerializer(news).data

    # Sports
    sports = Post.objects.filter(
        category__iexact="sports").order_by('-date_posted').first()
    sports = PostSerializer(sports).data

    # Science
    sci = Post.objects.filter(category__iexact="science").order_by(
        '-date_posted').first()
    sci = PostSerializer(sci).data

    # Entertainment
    ent = Post.objects.filter(category__iexact="entertainment").order_by(
        '-date_posted').first()
    ent = PostSerializer(ent).data

    data = {
        "Tech": tech,
        "News": news,
        "Sports": sports,
        "Science": sci,
        "Entertainment": ent,
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_post_view(request, *args, **kwargs):

    account = User.objects.get(id=1)

    blog_post = Post(author=account)

    if request.method == 'POST':
        serializer = PostSerializer(blog_post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# post hashtag
@api_view(['GET'])
def api_post_hashtag_view(request, pk, *args, **kwargs):
    data = {}
    qs = Post.objects.filter(id=pk).first().title
    qs = Tag.objects.filter(post__iexact=qs).all()
    if qs.exists():
        data = [x.serialize() for x in qs]
        return Response(data)
    return Response(data, status=status.HTTP_404_NOT_FOUND)
