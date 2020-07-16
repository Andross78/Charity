from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy

from .models import Donation, Institution, Category, User
from .forms import UserCreateForm, UserLoginForm, AddDonatForm, UserEditForm, MailForm

class LandingPageView(View):
    template_name = 'charity_app/index.html'
    def get(self, request):
        institutions = Institution.objects.all()
        donats = Donation.objects.all()
        fun = Institution.objects.filter(type=0)
        org_poz = Institution.objects.filter(type=1)
        zb_lok = Institution.objects.filter(type=2)
        context = {
            'institutions': institutions,
            'donats': donats,
            'fun': fun,
            'org_poz': org_poz,
            'zb_lok': zb_lok,
        }
        return render(request, self.template_name, context)


class AddDonationView(View):
    template_name = 'charity_app/form.html'
    success_url = reverse_lazy('confirmation')
    form_class = AddDonatForm
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            donat = Donation.objects.create(
                quantity=int(form.cleaned_data['bags']),
                institution=Institution.objects.get(id=form.cleaned_data['institution']),
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['postcode'],
                phone_number=form.cleaned_data['phone'],
                pick_up_date=form.cleaned_data['data'],
                pick_up_time=form.cleaned_data['time'],
                pick_up_comment=form.cleaned_data['more_info'],
                user=User.objects.get(pk=self.request.user.id),
            )
            categories = form.cleaned_data['category']
            for cat in categories:
                donat.categories.add(Category.objects.get(id=cat))
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponse(form.errors)



class DonatConfirmView(View):
    template_name = 'charity_app/form-confirmation.html'
    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'charity_app/login.html'
    def get(self, request):
        return render(request, self.template_name)


class RegisterView(FormView):
    form_class = UserCreateForm
    success_url = '/login'
    template_name = 'charity_app/register.html'
    def form_valid(self, form):
        new_user = form.instance
        new_user.username = form.cleaned_data['email']
        password = form.cleaned_data["password"]
        new_user.set_password(password)
        new_user.save()
        return super().form_valid(form)


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'charity_app/login.html'
    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email, password=password)
        if user:
            login(self.request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/register')


class UserLogoutView(LogoutView):
    ...


class ProfileView(View):
    template_name = 'charity_app/profile.html'
    success_url = reverse_lazy('profile')
    def get(self, request):
        donations = Donation.objects.filter(user=self.request.user).filter(is_take=False)
        donations_not_taken = Donation.objects.filter(user=self.request.user).filter(is_take=True)
        context = {
            'donations': donations,
            'donations_not_taken': donations_not_taken,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        donations = Donation.objects.filter(user=self.request.user).filter(is_take=False)
        for donat in donations:
            is_taken = request.POST['is_taken']
            donat.is_take = True if is_taken == 'on' else False
            donat.save()
            return HttpResponseRedirect(self.success_url)


class ProfileEditView(View):
    class_form = UserEditForm
    template_name = 'charity_app/profile_edit.html'
    success_url = reverse_lazy('base')

    def get(self, request):
        form = self.class_form
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.class_form(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if authenticate(username=self.request.user.email, password=password):
                if first_name or last_name or email:
                    self.request.user.first_name = first_name
                    self.request.user.last_name = last_name
                    self.request.user.email = email
                    self.request.user.save()
                    return HttpResponseRedirect(self.success_url)
                elif new_password and confirm_password and new_password == confirm_password:
                    self.request.user.set_password(new_password)
                    self.request.user.save()
                    user = authenticate(username=self.request.user.email, password=new_password)
                    if user:
                        login(self.request, user)
                    return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponse(form.errors)

class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name_suffix = '_update_form'


class SendMailView(View):
    form_class = MailForm
    template_name = 'charity_app/base.html'

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            title = 'Test message'
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            message = f'Wiadomosc od {name} {surname}\n'
            message += form.cleaned_data['message']
            send_mail(title,
                      message,
                      'wdsasha22@gmail.com',
                      ['wdsasha22@gmail.com'])
            return HttpResponseRedirect(reverse_lazy('base'))