from rest_framework import serializers
from users.models import Post
from taggit.serializers import (TagListSerializerField, TaggitSerializer)


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    hashtags = TagListSerializerField()

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
            'hashtags',
            'likes',
            'dislikes',
            'views',
            'date_posted',
        ]
        read_only_fields = ['pk', 'author', 'date_posted']

    # validations for data passed
    def get_url(self, obj):
        request = self.context.get('request')
        abs_url = obj.get_absolute_url()
        return request.build_absolute_uri(abs_url)

    def get_dislikes(self, obj):
        return obj.dislikes.count()

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_title(self, value):
        qs = Post.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("The title must be unique")
        return value
