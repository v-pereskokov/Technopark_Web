# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ask.models import Question, Tag
from random import choice, randint
from faker import Factory
import os

class Command(BaseCommand):
    help = 'Creates questions'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                action='store',
                dest='number',
                default=1000,
                help='Number of questions to add'
        )

    def handle(self, *args, **options):
        fake = Factory.create()

        number = int(options['number'])

        users = User.objects.all()[1:]

        starts = (
                'How do I Sort a Multidimensional',
                'What is Vlad?',
                'SQL Server'
                )

        for i in range(0, number):
            q = Question()

            q.title = fake.sentence(nb_words=randint(2, 4), variable_nb_words=True)
            q.text = u"%s %s %s" % (
                    choice(starts),
                    os.linesep,
                    fake.paragraph(nb_sentences=randint(1, 4), variable_nb_sentences=True),
                    )
            q.user = choice(users)
            q.rating = randint(0, 1500)
            q.is_published = True
            q.id = i
            q.save()
            self.stdout.write('add question [%d]' % (q.id))
