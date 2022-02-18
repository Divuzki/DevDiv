from rest_framework import serializers
from users.models import Post


class PostSerializer(serializers.ModelSerializer):
    url  = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = [
            'url',
            'author',
            'title',
            'description',
            'image_url',
            'video_url',
            'content',
            'category',
            'hashtag',
            'likes',
            'dislikes',
            'date_posted',
        ]
        read_only_fields = ['pk','author','date_posted']

    # validations for data passed
    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)
    
    def validate_title(self, value):
        qs = Post.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("The title must be unique")
        return value
