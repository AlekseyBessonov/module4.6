from django.forms import ModelForm
from .models import Post
from django.contrib.auth.models import User



# Создаём модельную форму
class NewsForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['title', 'text', 'categoryType', 'author', 'postCategory']



class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email']