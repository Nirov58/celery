from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        posts = Post.objects.filter(author=self.pk)
        posts_rating = 0
        for p in posts:
            posts_rating += p.rating*3
        comments = Comment.objects.filter(user=self.user_id)
        comments_rating = 0
        for c in comments:
            comments_rating += c.rating
        p_coms_rating = 0
        for i in posts.values("id"):
            p_coms = Comment.objects.filter(post=i["id"])
            for c in p_coms:
                p_coms_rating += c.rating
        new_rating = posts_rating + comments_rating + p_coms_rating
        self.user_rating = new_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategoryUser')

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    news = 'NWS'
    article = 'ART'

    TYPES = [
        (news, 'News'),
        (article, 'Article')
    ]

    type = models.CharField(max_length=3, choices=TYPES)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    name = models.CharField(max_length=255, default="Good news, everyone!")
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124]+"..."

    def get_absolute_url(self):
        return reverse('news_item', args=[str(self.pk)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class CategoryUser(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
