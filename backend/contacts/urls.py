from django.urls import path
from . import views

urlpatterns = [
    path("", views.Contacts.as_view()),
    path("<int:pk>", views.ContactsDetail.as_view()),
    path("<int:pk>/labels", views.ContactLabels.as_view()),
    path("labels", views.Labels.as_view()),
    # template 용
    path("template", views.ContactsTemplate.as_view()),
    path("<int:pk>/template", views.ContactsDetailTemplate.as_view()),
]
