from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import ArticleFilter
from .forms import ArticleForm
from .models import Article, Subscription, Author

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


class ArticlesList(ListView):
    model = Article
    ordering = 'title'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticleFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = 'article.html'
    context_object_name = 'article'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'simpleapp.add_article'
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'simpleapp.change_article'
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'
    pk_url_kwarg = 'id'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'simpleapp.delete_article'
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    pk_url_kwarg = 'id'


class ArticleSearch(ListView):
    model = Article
    template_name = 'article_search.html'
    context_object_name = 'articles'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticleFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
@csrf_protect

def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Author.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Author.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )