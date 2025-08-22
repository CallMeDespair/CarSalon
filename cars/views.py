from django.http import Http404
from django.views.generic import DetailView, ListView
from cars.models import Cars
from cars.utils import q_search
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.http import HttpResponseRedirect


class CatalogView(ListView):
    model = Cars
    template_name = "cars/catalog.html"
    context_object_name = "goods"
    paginate_by = 50
    allow_empty = True
    slug_url_kwarg = "category_slug"

    def get_queryset(self):
        category_slug = self.kwargs.get(self.slug_url_kwarg)
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if category_slug == "all":
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != "default":
            goods = goods.order_by(order_by)

        if min_price:
            goods = goods.filter(price__gte=min_price)
        if max_price:
            goods = goods.filter(price__lte=max_price)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Каталог"
        context["slug_url"] = self.kwargs.get(self.slug_url_kwarg)
        return context



class ProductView(DetailView):
    # model = Products
    # slug_field = "slug"
    template_name = "cars/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_object(self, queryset=None):
        product = Cars.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context


class CarCreateView(UserPassesTestMixin, CreateView):
    model = Cars
    template_name = 'cars/car_form.html'
    fields = ['name', 'category', 'description', 'image', 'price', 'discount', 'quantity']

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        # Автоматически создаем slug из названия перед сохранением
        instance = form.save(commit=False)
        instance.slug = slugify(instance.name)
        instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cars:index', kwargs={'category_slug': 'all'})


class CarUpdateView(UserPassesTestMixin, UpdateView):
    model = Cars
    template_name = 'cars/car_form.html'
    fields = ['name', 'category', 'description', 'image', 'price', 'discount', 'quantity']
    slug_url_kwarg = 'product_slug'

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('cars:product', kwargs={'product_slug': self.object.slug})


class CarDeleteView(UserPassesTestMixin, DeleteView):
    model = Cars
    success_url = reverse_lazy('cars:index', kwargs={'category_slug': 'all'})
    slug_url_kwarg = 'product_slug'  # Убедитесь, что это соответствует вашему URL

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        # Блокируем удаление через GET-запрос
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        # Выполняем удаление при POST-запросе
        return self.delete(request, *args, **kwargs)