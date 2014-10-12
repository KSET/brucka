# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from tickets.models import Student


class Command(BaseCommand):
    args = '<students.txt>'
    help = 'Populate students based on specified txt file'

    option_list = BaseCommand.option_list + (
        make_option(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
        ),
    )

    @transaction.commit_on_success
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('You must provide file with students.')
        filename = args[0]
        dry_run = options['dry_run']

        lines = (line.rstrip() for line in open(filename))
        lines = (line.rstrip().strip() for line in lines if line)
        count = 0
        created_count = 0
        for line in lines:
            code = line
            if dry_run:
                created = not Student.objects.filter(code=code).exists()
            else:
                obj, created = Student.objects.get_or_create(code=line)
            count += 1
            if created:
                created_count += 1
        print 'Inserted items: %d of %d' % (created_count, count)
