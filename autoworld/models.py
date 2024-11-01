from django.db import models

class Dimensions(models.Model):
    Modelname = models.CharField(max_length=100, blank=True, null=True)
    Length = models.CharField(max_length=100, blank=True, null=True)
    Width = models.CharField(max_length=100, blank=True, null=True)
    Height = models.CharField(max_length=100, blank=True, null=True)
    Wheelbase = models.CharField(max_length=100, blank=True, null=True)
    Boot_Space = models.CharField(max_length=100, blank=True, null=True)
    Seating_Capacity = models.CharField(max_length=100, blank=True, null=True)
    Turning_Radius = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.Modelname

class YouTubeVideo(models.Model):
    model = models.ForeignKey(Dimensions, related_name='videos', on_delete=models.CASCADE, null=True)  # Allow nulls
    video_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    view_count = models.IntegerField()
    like_count = models.IntegerField()
    comment_count = models.IntegerField()

class YouTubeComment(models.Model):
    video = models.ForeignKey(YouTubeVideo, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    text = models.TextField()
    like_count = models.IntegerField()
    sentiment = models.CharField(max_length=10, null=True, choices=[('Positive', 'Positive'), ('Negative', 'Negative'), ('Neutral', 'Neutral')])
    category = models.CharField(max_length=10, null=True)

    class Meta:
        unique_together = ('video', 'text')

    def __str__(self):
        return f"{self.author}: {self.text[:20]}"

# New Models for Instagram and Twitter Posts and Comments

class InstagramPost(models.Model):
    model = models.ForeignKey(Dimensions, related_name='instagram_posts', on_delete=models.CASCADE)
    post_id = models.CharField(max_length=20, unique=True)
    image_url = models.URLField(max_length=200)  # URL of the post image
    caption = models.TextField()
    like_count = models.IntegerField()
    comment_count = models.IntegerField()

    def __str__(self):
        return f"Instagram Post: {self.post_id} - {self.caption[:20]}"

class InstagramComment(models.Model):
    post = models.ForeignKey(InstagramPost, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    text = models.TextField()
    like_count = models.IntegerField()
    sentiment = models.CharField(max_length=10, null=True, choices=[('Positive', 'Positive'), ('Negative', 'Negative'), ('Neutral', 'Neutral')])
    category = models.CharField(max_length=10, null=True)

    class Meta:
        unique_together = ('post', 'text')

    def __str__(self):
        return f"{self.author}: {self.text[:20]}"

class TwitterPost(models.Model):
    model = models.ForeignKey(Dimensions, related_name='twitter_posts', on_delete=models.CASCADE)
    post_id = models.CharField(max_length=20, unique=True)
    content = models.TextField()
    retweet_count = models.IntegerField()
    like_count = models.IntegerField()
    reply_count = models.IntegerField()

    def __str__(self):
        return f"Twitter Post: {self.post_id} - {self.content[:20]}"

class TwitterComment(models.Model):
    post = models.ForeignKey(TwitterPost, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    text = models.TextField()
    like_count = models.IntegerField()
    sentiment = models.CharField(max_length=10, null=True, choices=[('Positive', 'Positive'), ('Negative', 'Negative'), ('Neutral', 'Neutral')])
    category = models.CharField(max_length=10, null=True)

    class Meta:
        unique_together = ('post', 'text')

    def __str__(self):
        return f"{self.author}: {self.text[:20]}"
