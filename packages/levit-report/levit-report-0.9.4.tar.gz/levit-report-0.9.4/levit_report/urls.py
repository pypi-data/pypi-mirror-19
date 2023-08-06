from django.conf.urls import url

from .views import DocumentFileView, BulkDocumentFileView

urlpatterns = [
  url(r'^(?P<slug>[\w-]+)/(?P<object_id>[0-9]+)/$', DocumentFileView.as_view(), name='print'),
  url(r'^(?P<slug>[\w-]+)/$', BulkDocumentFileView.as_view(), name='print'),
]
