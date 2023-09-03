from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse
from django.db import models


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    # def __str__(self):
    #     return str(self.authorUser.username)

    def __str__(self):
        return self.authorUser.username

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()



class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribed = models.ManyToManyField(User, through='SubscribedUsersCategory')


    def __str__(self):
        return str(self.name)


class Post(models.Model):
    class Meta:
        ordering = ["-dateCreation"]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Покупка'),
        (ARTICLE, 'Продажа'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True,
                              default='/photos/def/1.jpg/')

    respond = models.ManyToManyField(User, through='Comment', related_name='post_comment')

    def __str__(self):
        return f'id: {self.id}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return str(self.text)[0:123] + '...'

    def __str__(self):
        return f'{self.author.authorUser.username},  {self.CATEGORY_CHOICES}, {self.dateCreation}'



    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'PostDetail-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class SubscribedUsersCategory(models.Model):
    subscribed = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post,  on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self):
        return self.postCategory.name



class Comment(models.Model):
    accept = True
    reject = False

    POSITION = [
        (reject, 'Отклонена'),
        (accept, 'Принята')

    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user_sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=accept, choices=POSITION)
    rating = models.SmallIntegerField(default=0)


    class Meta:
        ordering = ['dateCreation']


    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.user_sender)

    def get_absolute_url(self):
        return reverse('index', 'respond_list', args=[str(self.id)])


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()










