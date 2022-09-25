from django.urls import path
from todoapp import views

urlpatterns=[
    path("signup",views.SignUpView.as_view(),name="register"),
    path("",views.LogInView.as_view(),name="signin"), #empty matching this page
    path("home",views.IndexView.as_view(),name="index"),
    path("logout",views.SignOutView.as_view(),name="signout"),
    path("todos/add",views.TodoAddView.as_view(),name="add_todo"),
    path("todos/all",views.TodoListView.as_view(),name="todo-list"),
    path("todos/delete/<int:id>",views.delete_todo,name="delete-todo"),
    path("todos/detail/<int:pk>",views.TodoDetailView.as_view(),name="todo-detail"), #''pk since detailview inherited
    path("todos/change/<int:id>",views.TodoEditView.as_view(),name="edit-todo"),

]