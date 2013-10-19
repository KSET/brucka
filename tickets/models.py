# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver


class Student(models.Model):
    first_name = models.CharField('ime', max_length=30)
    last_name = models.CharField('prezime', max_length=30)
    username = models.CharField('username', max_length=30, unique=True)
    email = models.CharField('e-mail', max_length=30, unique=True)

    @property
    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @property
    def ticket_or_none(self):
        try:
            return self.ticket
        except ObjectDoesNotExist:
            return None

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'brucoš'
        verbose_name_plural = 'brucoši'
    def __unicode__(self):
        return self.full_name


class Ticket(models.Model):
    number = models.CharField('br. karte', max_length=30, unique=True)
    student = models.OneToOneField(Student, related_name='ticket')
    creation_time = models.DateTimeField('vrijeme prodaje', auto_now_add=True)

    class Meta:
        ordering = ['-creation_time']
        verbose_name = 'karta'
        verbose_name_plural = 'karte'
    def __unicode__(self):
        return u'Karta za %s' % unicode(self.student)

@receiver(pre_save, sender=Ticket)
def exam_gen_id(sender, instance, **kwargs):
    if instance.number:    # ako je update
        return
    qs = Ticket.objects.all().order_by('-number')
    if qs.exists():
        max_num = qs[0].number
        num = int(max_num.split('B')[1]) + 1
    else:
        num = 1
    instance.number = 'B%03d' % num
