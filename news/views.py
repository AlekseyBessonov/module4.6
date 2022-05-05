from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View
from .tasks import SendEmail
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, mail_managers
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, TemplateView
from .models import Post, Category, User, Author
from .filters import NewsFilter
from datetime import datetime
from .forms import NewsForm
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Post)
def notify_post_create(sender, instance, **kwargs):

    subject = f'{instance.title}'
    message = f'{instance.text} '
    userlist = []

    for usr in User.objects.all():
        subscribers = usr.email
        #print(11, subscribers)
        userlist.append(subscribers)

    send_mail(subject, message, 'hellraver81@yandex.ru', userlist)

    post_save.connect(notify_post_create, sender=Post)


class List(ListView):
    model = Post
    template_name = 'main.html'
    context_object_name = 'post'
    queryset = Post.objects.order_by('-createTime')
    paginate_by = 3


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'post'
    queryset = Post.objects.order_by('-createTime')
    form_class = NewsForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['form'] = NewsForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем
            form.save()

        return super().get(request, *args, **kwargs)


class PostDetailView(DetailView):
    permission_required = ('news.view_post')
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()

    def get_category(self, **kwargs):
        id = self.kwargs.get('pk')
        return Category.objects.get(pk=id)


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    permission_required = ('news.add_post')
    template_name = 'news/news_create.html'
    form_class = NewsForm


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'news/news_create.html'
    form_class = NewsForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'sign/author.html'
    context_object_name = 'author'


class RedisView(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')