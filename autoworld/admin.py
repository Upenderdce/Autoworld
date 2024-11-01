from django.contrib import admin
from autoworld.models import Dimensions
from .models import YouTubeVideo, YouTubeComment, InstagramPost, InstagramComment, TwitterPost, TwitterComment

# Inline class for YouTube Comments
class YouTubeCommentInline(admin.TabularInline):
    model = YouTubeComment
    extra = 1  # Number of empty forms to display

# Inline class for Instagram Comments
class InstagramCommentInline(admin.TabularInline):
    model = InstagramComment
    extra = 1  # Number of empty forms to display

# Inline class for Twitter Comments
class TwitterCommentInline(admin.TabularInline):
    model = TwitterComment
    extra = 1  # Number of empty forms to display

# Admin registration for Dimensions model
@admin.register(Dimensions)
class DimensionsAdmin(admin.ModelAdmin):
    list_display = ('Modelname', 'Length', 'Width', 'Height', 'Wheelbase')

# Admin registration for YouTube Video model
@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('model', 'title', 'view_count', 'like_count', 'comment_count')
    inlines = [YouTubeCommentInline]
    list_filter = ('model',)

# Admin registration for YouTube Comment model
@admin.register(YouTubeComment)
class YouTubeCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'video', 'sentiment', 'category')
    list_filter = ('video',)

# Admin registration for Instagram Post model
@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    list_display = ('model', 'post_id', 'like_count', 'comment_count', 'caption')
    inlines = [InstagramCommentInline]
    list_filter = ('model',)

# Admin registration for Instagram Comment model
@admin.register(InstagramComment)
class InstagramCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'post', 'sentiment', 'category')
    list_filter = ('post',)

# Admin registration for Twitter Post model
@admin.register(TwitterPost)
class TwitterPostAdmin(admin.ModelAdmin):
    list_display = ('model', 'post_id', 'content', 'like_count', 'retweet_count', 'reply_count')
    inlines = [TwitterCommentInline]
    list_filter = ('model',)

# Admin registration for Twitter Comment model
@admin.register(TwitterComment)
class TwitterCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'post', 'sentiment', 'category')
    list_filter = ('post',)