from django.urls import path

from .views import NewsList, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, List, AuthorDetail
# импортируем наше представление

urlpatterns = [
        path('', List.as_view()),  #ссылка на список
        path('search/', NewsList.as_view()), # ссылк ана страницу поиска
        path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Ссылка на подробности
        path('create/', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание
        path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'), #удаление
        path('update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),  # Ссылка на обновление
        path('author/', AuthorDetail.as_view(), name='author'),
#
    ]
