from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        comRating = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += comRating.get('commentRating')
        self.ratingAuthor = cRat + pRat
        self.save()

    def __str__(self):
        return str(self.authorUser)


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscription')

    def __str__(self):
        return '{}'.format(self.name)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'

    CATEGORY_CHOICE = (
        (NEWS, 'Новости'),
        (ARTICLE, 'Статья'),
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICE, default=ARTICLE)
    createTime = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title

    #  def __str__(self):
    #      return self.author.authorUser

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return '{}...'.format(self.text[0:123])

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/{self.id}'


class PostCategory(models.Model):
    postThrought = models.ForeignKey(Post, on_delete=models.CASCADE)
    postCategory = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creationTime = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
