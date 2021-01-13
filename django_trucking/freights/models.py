from django.db import models
from datetime import date

from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Worker(models.Model):
    """Диспетчеры и водители"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="workers/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('worker_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Диспетчеры и водители"
        verbose_name_plural = "Диспетчеры и водители"


class Type(models.Model):
    """Типы"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Типы"
        verbose_name_plural = "Типы"


class Freight(models.Model):
    """Грузоперевозка"""
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="freights/")
    year = models.PositiveSmallIntegerField("Дата загрузки", default=2021)
    city = models.CharField("Загрузка", max_length=30)
    directors = models.ManyToManyField(Worker, verbose_name="диспетчер", related_name="freight_director")
    workers = models.ManyToManyField(Worker, verbose_name="водители", related_name="freight_worker")
    types = models.ManyToManyField(Type, verbose_name="типы")
    world_premiere = models.DateField("Дата выгрузки", default=date.today)
    budget = models.PositiveIntegerField("Тариф", default=0,
                                         help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указывать сумму в долларах"
    )
    fess_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("freight_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Грузоперевозка"
        verbose_name_plural = "Грузоперевозки"


class Details(models.Model):
    """Детали"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    freight = models.ForeignKey(Freight, verbose_name="Грузоперевозка", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Детали"
        verbose_name_plural = "Детали"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    freight = models.ForeignKey(Freight, on_delete=models.CASCADE, verbose_name="грузоперевозка", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.freight}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    freight = models.ForeignKey(Freight, verbose_name="грузоперевозка", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.freight}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"