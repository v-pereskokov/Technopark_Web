# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models import Count
from django.utils import timezone
import datetime


class QuestionManager(models.Manager):
	def newest(self):
		return self.order_by('-data')

	def hot(self):
		return self.order_by('-rating')

	def tag_search(self, input_tag):
		return self.filter(tags__text=input_tag)

	def published(self):
		return self.filter(is_published=True)

	def user_questions(self, user_name):
		return self.filter(user__username=user_name)

	def date_search(self, date):
		return self.filter(date=date)


class ProfileManager(models.Manager):
	def get_by_name(self, user_name):
		return self.filter(user__username=user_name)


class TagManager(models.Manager):
	def with_question_count(self):
		return self.annotate(questions_count=Count('question'))

	def order_by_question_count(self):
		return self.with_question_count().order_by('-questions_count')

	def order_by_name_with_question_count(self):
		return self.with_question_count().order_by('text')

	def get_popular_tags(self):
		return self.order_by_question_count().all()[:10]


class Tag(models.Model):
	class Meta:
		verbose_name = u'Тэг'
		verbose_name_plural = u'Тэги'

	text = models.CharField(max_length=50, verbose_name=u'Тег', unique=True)
	style_number = models.IntegerField(default=1, verbose_name=u'Номер')
	objects = TagManager()

	def __unicode__(self):
		return self.text


class Question(models.Model):
	class Meta:
		verbose_name = u'Вопрос'
		verbose_name_plural = u'Вопросы'

	user = models.ForeignKey(User, verbose_name=u'Пользователь')
	title = models.CharField(max_length=255, verbose_name=u'Заголовок')
	text = models.TextField(verbose_name=u'Текст')
	rating = models.IntegerField(default=0, verbose_name=u'Рейтинг')
	is_published = models.BooleanField(default=False, verbose_name=u'Опубликована')
	data = models.DateTimeField(default=timezone.now, verbose_name=u'Дата создания')
	tags = models.ManyToManyField(Tag, verbose_name=u'Тэг')
	objects = QuestionManager()

	def get_absolute_url(self):
		return '/question/id%d/' % self.id

	def __unicode__(self):
		return self.title


class Answer(models.Model):
	class Meta:
		verbose_name = u'Ответ'
		verbose_name_plural = u'Ответы'

	user = models.ForeignKey(User, verbose_name=u'Пользователь')
	question = models.ForeignKey(Question, verbose_name=u'Вопрос')
	text = models.TextField(verbose_name=u'Текст')
	rating = models.IntegerField(default=0, verbose_name=u'Рейтинг')
	data = models.DateTimeField(default=timezone.now, verbose_name=u'Дата добавления')
	is_correct = models.BooleanField(default=False, verbose_name=u'Корректность')
	id = models.IntegerField(primary_key=True, verbose_name=u'id')


class QuestionLikeManager(models.Manager):
	def like(self, id, user):
		compose_key = str(user) + str(id)
		question = Question.objects.get(pk=id)
		try:
			qLike = QuestionLike.objects.get(compose_key=compose_key)
		except QuestionLike.DoesNotExist:
			qLike = QuestionLike.objects.create(compose_key=compose_key)
			qLike.question = question
			user.profile.questionlikes.add(qLike)
			user.profile.save()
		question.save()
		question.user.profile.save()
		qLike.save()
		return qLike


class QuestionLike(models.Model):
	class Meta:
		verbose_name = u'Рейтинг вопроса'
		verbose_name_plural = u'Рейтинг вопросов'

	value = models.IntegerField(default=0)
	question = models.ForeignKey(Question, default=0)
	compose_key = models.CharField(max_length=70, unique=True, default='None0')
	is_liked = models.BooleanField(default=False)

	objects = QuestionLikeManager()

	def __unicode__(self):
		return str(self.value)


class Profile(models.Model):
	class Meta:
		verbose_name = u'Профиль'
		verbose_name_plural = u'Профили'

	user = models.OneToOneField(User, verbose_name=u'Пользователь')
	avatar = models.ImageField(upload_to='uploads', default="uploads/user_2.png")
	information = models.TextField(default="My info", verbose_name=u'Информация')
	rating = models.IntegerField(default=0, verbose_name=u'Рейтинг')
	questionlikes = models.ManyToManyField(QuestionLike)

	objects = ProfileManager()

	def __unicode__(self):
		return unicode(self.user)
