from django.shortcuts import render,redirect

# Create your views here.

from myapp.forms import TaskForm,RegistrationForm,SignInForm

from django.views.generic import View

from myapp.models import Task

from django.contrib import messages

from django import forms

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout





class TaskCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TaskForm()

        return render(request,"taskcreate.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=TaskForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user=request.user

            form_instance.save()

            messages.success(request,"created suucessfully")

            return redirect("task_create")

        else:

            messages.error(request,"creation failed")

            return render(request,"taskcreate.html",{"form":form_instance})


class TaskListView(View):

    def get(self,request,*args,**kwargs):

        search_text=request.GET.get("search_text")         

        selected_category=request.GET.get("category","all")

        if selected_category =="all":

            qs=Task.objects.all()

        else:

            qs=Task.objects.filter(category=selected_category)    

        if search_text!=None:

            qs=Task.objects.filter(Q(title_icontains=search_text)|Q(description_contains=search_text))       

        return render(request,"task_list.html",{"tasks":qs,"selected":selected_category})


class TaskDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Task.objects.get(id=id)

        return render(request,"task_detail.html",{"task":qs})


class TaskUpdateView(View):

    def get(self,request,*args,**kwargs):

        # extract pk from kwargs

        id=kwargs.get("pk")

        task_obj=Task.objects.get(id=id)

        form_instance=TaskForm(instance=task_obj)

        form_instance.fields["status"]=forms.ChoiceField(choices=Task.status_choices,widget=forms.Select(attrs={"class":"form-control form-select"}))

        return render(request,"taskupdate.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        form_instance=TaskForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            status=request.POST.get("status")

            Task.objects.filter(id=id).update(**data,status=status)

            messages.success(request,"update successfully")

            return redirect("task_list")
        
        else:

            messages.error(request,"update failed")

            return render(request,"taskupdate.html",{"form":form_instance})


class TaskDeleteView(View):

    def get(self,request,*args,**kwargs):

        Task.objects.get(id=kwargs.get("pk")).delete()

        messages.success(request,"deleted successfully")

        return redirect("task_list")


class TaskSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Task.objects.all()

        total_task_count=qs.count()

        context={

        }

        return render(request,"task_summary.html",context)



class SignUpView(View):

    template_name="register.html"

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            return redirect("task_list")

        else:

            return render(request,self.template_name,{"form":form_instance})


class SignInView(View):

    template_name="signin.html"

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")    

            pswrd=form_instance.cleaned_data.get("password")

            user_obj=authenticate(request,username=uname,password=pswrd)

            if user_obj:

                login(request,user_obj)

                return redirect("task_list")

        return render(request,self.template_name,{"form":form_instance})


class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")


    





