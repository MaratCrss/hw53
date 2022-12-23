from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from accounts.forms import MyUserCreationForm


class RegisterView(CreateView):
    model = User
    template_name = 'create_user.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:projects')
        return next_url

# def login_view(request):
#     context = {}
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('webapp:index')
#         else:
#             context['has_error'] = True
#     return render(request, 'login.html', context=context)
#
# def logout_view(request):
#     logout(request)
#     return redirect('webapp:index')