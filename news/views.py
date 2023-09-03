from datetime import datetime
from .filters import PostFilter, RequestsFilter
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from .forms import *
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, Http404
from django.core.mail import send_mail



#главная страница
class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    gueryset = Post.objects.order_by('-id')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()

        return context



#найти новость или статью, фильтрация, пагинация

class SearchPosts(ListView):
    paginate_by = 3
    model = Post
    ordering = '-dateCreation'
    template_name = 'post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = PostFilter(self.request.GET, queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


#подробности о статье или новости:
class PostDetail(DetailView):
    model = Post
    template_name = 'id.news.html'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_category'] = Category.objects.filter(subscribed=self.request.user)

            context['posts'] = Post.objects.filter(author__authorUser__username=self.request.user),
            context['comments'] = Comment.objects.filter(post__author__authorUser__username=self.request.user)
        else:
            context['user_category'] = None
            context['posts'] = None
            context['comments'] = None

        return context


# кеширование
#     def get_object(self, *args, **kwargs):
#         obj = cache.get(f"PostDetail-{self.kwargs['pk']}", None)
#
#         if not obj:
#             obj = super().get_object(queryset=self.get_queryset())
#             cache.set(f"PostDetail-{self.kwargs['pk']}", obj)
#
#         return obj

# комментарии

@login_required
@csrf_protect
def responds(request,  **kwargs):
        # success_url = '/news/'
        # template_name = 'id.news.html'
        post = get_object_or_404(Post, pk=kwargs['pk'])
        # Fetching the comments that have active=True
        comments = post.comments.filter(active=True)
        new_comment = None


        # Comment posted
        if request.method == 'POST':

            comment_form = CreateCommentForm(data=request.POST)
            if comment_form.is_valid():
                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.post = post
                # Save the comment to the database
                new_comment.save()

                email = request.user.email
                body = f"Уважаемый {post.author.authorUser.username}!\n " \
                       f" У вас появились новые комментарии на Ваш пост :  {post.title}.\n" \
                       f"Вы можете перейти в личный кабинет на сайте NewsPaper: http://127.0.0.1:8000\n" \
                       f"где сможете одобрить или отказать данный отклик"

                send_mail('new_comment', body, 'usjusj@yandex.ru', [email],  fail_silently=False)


        else:
            comment_form = CreateCommentForm()

            print('Comments:', comments)
            return render(request,
                          'respond_create.html',
                          {'post': post,
                           'comments': new_comment,
                           'new_comment': new_comment,
                           'comment_form': comment_form})

        return redirect('/news/')



class ResponseListView(LoginRequiredMixin, ListView):
    context_object_name = 'responses'
    model = Comment
    template_name = 'respond_list.html'
    ordering = '-dateCreation'



class ResponceListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'respond_list.html'
    # context_object_name = 'respond_list'
    ordering = '-dateCreation'

    paginate_by = 3
    context_object_name = 'comments'

# одобряем или отклоняем комментарий
    def post(self, request, *args, **kwargs):
        action = None
        action = request.POST.get('action')
        comment = Comment.objects.get(id=Comment.objects.get(id=request.POST.get('post_id')).id)

        if action == 'accept':
            comment.active = 'True'
            comment.save()
        elif action == 'reject':
            comment.active = 'False'
            comment.save()
        # return redirect(to='/')
        return redirect('respond_list')



# фильтруем комментарии


    def get_queryset(self):
            queryset = super().get_queryset()
            self.filter = RequestsFilter(self.request.GET, queryset)
            return self.filter.qs

    def get_context_data(self,  **kwargs) -> dict:
            context = super().get_context_data(**kwargs)
            context['filter'] = self.filter
            context['posts'] = Post.objects.filter(author__authorUser__username=self.request.user)
            context['comment'] = Comment.objects.filter(post__author__authorUser__username=self.request.user)
            context['active'] = self.request.GET.get('active')

            active = self.request.GET.get('active')
            if active == 'True':
                context['active'] = Comment.objects.filter(post__author__authorUser__username=self.request.user, active= active)
            elif active == 'False':
                context['active'] = Comment.objects.filter(post__author__authorUser__username=self.request.user, active= active)
            else:
                context['active'] = Comment.objects.filter(post__author__authorUser__username=self.request.user)

            return context





# создаем:

class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm
    context_object_name = 'post_create'
    success_url = '/news/'
    login_url=reverse_lazy('login')
    permission_required = ('news.add_post')
    # raise_exception = True



# удаляем
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all
    success_url = '/news/'

    login_url = reverse_lazy('login')
    permission_required = ('news.delete_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

# редактируем
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm
    context_object_name = 'post_edit'
    success_url = '/news/'
    login_url = reverse_lazy('login')
    permission_required = ('news.change_post')



def subscription(request):
    category_id = request.GET.get('category_id')
    category = Category.objects.get(id=category_id)
    if not category.subscribed.filter(email=request.user.email).exists():
        user = request.user
        SubscribedUsersCategory.objects.create(subscribed=user, category=category)
    return redirect('/')




















