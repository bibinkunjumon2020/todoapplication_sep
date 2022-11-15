from django.urls import path
from app.views import TodosView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("todos",TodosView,basename="todos")


urlpatterns=[

]+router.urls
