from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import NewFilter
from .forms import NewForm
from simpleapp.models import New, Subscription, Author

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


class NewsList(ListView):
    model = New
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewDetail(DetailView):
    model = New
    template_name = 'new.html'
    context_object_name = 'new'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'simpleapp.add_new'
    form_class = NewForm
    model = New
    template_name = 'new_edit.html'


class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'simpleapp.change_new'
    form_class = NewForm
    model = New
    template_name = 'new_edit.html'
    pk_url_kwarg = 'id'


class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'simpleapp.delete_new'
    model = New
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')
    pk_url_kwarg = 'id'


class NewSearch(ListView):
    model = New
    template_name = 'new_search.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        author_id = request.POST.get('author_id')
        author = Author.objects.get(id=author_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, author=author)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                author=author
            ).delete()

    authors_with_subscriptions = Author.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                author=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'authors': authors_with_subscriptions},
    )


