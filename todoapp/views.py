from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView
from todoapp import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from todoapp.models import Todos
from django.contrib import messages
from django.urls import reverse_lazy
from .decorators import signin_required
from django.utils.decorators import method_decorator

# Create your views here.

# registration
# login
# add
# list
# update
# delete
'''
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=forms.RegistrationForm()
        return render(request,"registration.html",context={"form":form})

    def post(self,request,*args,**kwargs):
        #print(request.POST)
        #print(request.POST.get("lastname"))
        form=forms.RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)  # here serializer method create_user not present.so form.save wont hash password.in that case we cannt use authentication
            messages.success(request, "Successfully Registered as a User")
            return redirect("signin") #name given in urls
        else:
            messages.error(request, "Failed to Register")
            return render("registration.html",context={"form":form})


        #return render(request,"login.html")
'''


class SignUpView(CreateView):
    template_name = "registration.html"
    # for post
    model = User
    form_class = forms.RegistrationForm
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request, "Successfully Registered as a User")
        return super().form_valid(form)


class LogInView(View):
    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        return render(request, "login.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        # print(request.POST.get("username"))
        # print(request.POST.get("password"))
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                print(request.user)  # this only works if login function used above
                print("success")
                messages.success(request, "Successfully Logged In")
                return redirect("index")
            else:
                print("failure")
                messages.error(request, "Failed to LogIn")
                return render(request, "login.html", context={"form": form})
        return render(request, "registration.html")


'''
class IndexView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"home.html")
'''


@method_decorator(signin_required, name="dispatch")
class IndexView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todos"] = Todos.objects.filter(user=self.request.user, status=False)
        return context


@method_decorator(signin_required, name="dispatch")
class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        print("loggged out")
        return redirect("signin")


'''
class TodoAddView(View):
    def get(self,request,*args,**kwargs):
        form = forms.TodoForm()
        return render(request,"add_todo.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=forms.TodoForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            #Todos.objects.create(**form.cleaned_data,user=request.user)
            messages.success(request, "Successfully Added one Todo ")
            return redirect("index")
        else:
            messages.error(request, "Failed to Add a TODO")
            return render(request,"add_todo.html",{"form":form})
            '''


@method_decorator(signin_required, name="dispatch")
class TodoAddView(CreateView):
    model = Todos
    form_class = forms.TodoForm
    template_name = "add_todo.html"
    success_url = reverse_lazy("todo-list")

    def form_valid(self, form):  # its overriden to add 'user' instance
        form.instance.user = self.request.user
        messages.success(self.request, "Successfully Added one Todo ")
        return super().form_valid(form)


"""
class TodoListView(View):
    def get(self,request,*args,**kwargs):
        todos = Todos.objects.all()
        return render(request,"todolist.html",{"todos":todos})
"""


@method_decorator(signin_required, name="dispatch")
class TodoListView(ListView):
    model = Todos
    context_object_name = "todos"
    template_name = "todolist.html"

    def get_queryset(self):  # overloading fn
        return Todos.objects.filter(user=self.request.user)  # query has no request


@signin_required
def delete_todo(request, *args, **kwargs):  # path : todos/delete/<int:id>
    id = kwargs.get("id")
    Todos.objects.get(id=id).delete()
    messages.success(request, "Successfully Deleted a Todo")
    return redirect("todo-list")


'''
class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        todo = Todos.objects.get(id=id)
        return render(request,"todo-detail.html",{"todo":todo})
'''


@method_decorator(signin_required, name="dispatch")
class TodoDetailView(DetailView):
    model = Todos
    context_object_name = "todo"
    template_name = "todo-detail.html"
    # pk_url_kwarg = "id"  i used pk in url


@method_decorator(signin_required, name="dispatch")
class TodoEditView(UpdateView):
    model = Todos
    template_name = "todo_edit.html"
    form_class = forms.TodoChangeForm
    success_url = reverse_lazy("todo-list")
    pk_url_kwarg = "id"

    def form_valid(self, form):
        messages.success(self.request, "Successfully Edited the Todo List ")
        return super().form_valid(form)

    '''
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        todo = Todos.objects.get(id=id)
        form = forms.TodoChangeForm(instance=todo)
        return render(request,"todo_edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        todo = Todos.objects.get(id=id)
        form = forms.TodoChangeForm(request.POST,instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully Edited the Todo List ")
            return redirect("todo-list")
        else:
            messages.error(request,"Failed to Edit")
            return render(request, "todo_edit.html", {"form": form})
    '''


from .models import Bird,Animal,Human
from .forms import BirdFormSet,AnimalFormSet,HumanFormSet


class BirdListView(ListView):
    model = Bird
    template_name = "bird_list.html"


# View for adding birds
class BirdAddView(TemplateView):
    template_name = "add_bird1.html"

    # Define method to handle GET request
    def get(self, *args, **kwargs):
        # Create an instance of the formset
        formset = BirdFormSet(queryset=Bird.objects.none(),prefix="bird")
        formset_animal=AnimalFormSet(queryset=Animal.objects.none(),prefix="animal")
        formset_human=HumanFormSet(queryset=Human.objects.none(),prefix="human")
        return self.render_to_response({'formset': formset,'formset_animal':formset_animal,'formset_human':formset_human})
        # Define method to handle POST request

    def post(self, *args, **kwargs):
        print(self.request.POST)

        formset = BirdFormSet(self.request.POST,prefix="bird")
        formset_animal=AnimalFormSet(self.request.POST,prefix="animal")
        formset_human=HumanFormSet(self.request.POST,prefix="human")

        print("?????????????????")
        print(formset)
        print("///////////////")
        print(formset_animal)
        # Check if submitted forms are valid
        if formset.is_valid() and formset_animal.is_valid() and formset_human.is_valid() :
            formset.save()
            formset_animal.save()
            formset_human.save()
            return redirect(reverse_lazy("bird_list"))

        return self.render_to_response({'bird_formset': formset})
