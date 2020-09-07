from rest_framework import serializers

from users.models import Post as BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlogPost
		fields = ['title','author', 'content', 'image_url','category','data_posted']







