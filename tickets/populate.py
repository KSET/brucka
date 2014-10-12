#!/usr/bin/env python
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    from os import sys, environ
    from os.path import dirname, abspath
    environ['DJANGO_SETTINGS_MODULE'] = 'brucka.settings'
    PROJECT_PATH = dirname(dirname(abspath(__file__)))
    sys.path.append(PROJECT_PATH)

from datetime import datetime
from django.db import transaction
from tickets.models import Student


@transaction.commit_on_success
def main(argv=[]):
    if len(argv) != 1:
        print 'You must provide file with students.'
        sys.exit(1)
    # Ivan, Horvat, ih12345, ivan.horvat@fer.hr
    lines = (line.rstrip() for line in open(argv[0]))
    lines = (line for line in lines if line)
    count = 0
    created_count = 0
    for data in (line.split(', ') for line in lines):
        obj, created = Student.objects.get_or_create(
            first_name=data[0], last_name=data[1], username=data[2], email=data[3])
        count += 1
        if created:
            created_count += 1
    print 'Inserted items: %d of %d' % (created_count, count)
    print datetime.now().strftime('Job ended: %Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    argv = sys.argv[1:]
    sys.exit(main(argv))
