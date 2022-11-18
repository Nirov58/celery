from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Post, Category
from .filters import NewsFilter
from .forms import NewsForm
from .exceptions import LimitError


class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsItem(DetailView):
    model = Post
    template_name = 'news_item.html'
    context_object_name = 'news_item'


class NewsSearch(NewsList):
    template_name = 'news_search.html'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news_portal_app.add_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def post(self, request, *args, **kwargs):
        try:
            super(NewsCreate, self).post(request.build_absolute_uri())
        except LimitError:
            return redirect('/news/limit')
        return redirect('/')

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'news' in self.request.build_absolute_uri():
            post.type = Post.news
        elif 'article' in self.request.build_absolute_uri():
            post.type = Post.article

        return super().form_valid(form)


def news_limit(request):
    return render(request, 'news_limit.html')


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news_portal_app.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    context_object_name = 'news_create'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class NewsInCategory(NewsList):
    template_name = 'news_category.html'
    context_object_name = 'news_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.request.path_info.split('/')[-1]
        context['category'] = Category.objects.get(pk=context['category_id'])
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.add(user)
    return redirect(f'../category/{pk}')


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(user)
    return redirect(f'../category/{pk}')
