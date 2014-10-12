from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = patterns(
    'tickets.views',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('tickets:student_list')), name='home'),
    url(r'^student/$', 'student_list', name='student_list'),
    url(r'^student/export/$', 'student_export', name='student_export'),
    url(r'^student/(?P<student_id>\d+)/$', 'student_detail', name='student_detail'),
    url(r'^student/(?P<student_id>\d+)/buy-ticket/$', 'student_buy_ticket', name='student_buy_ticket'),
    url(r'^student/(?P<student_id>\d+)/send-email/$', 'student_send_mail', name='student_send_mail'),
)
