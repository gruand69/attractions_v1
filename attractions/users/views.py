from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy

from posts.models import Post
from users.forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class UserCreateView(CreateView):
    model = User
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    # success_url = reverse_lazy('users:profile')

    def get_success_url(self) -> str:
        # print(self.request.user.username)
        return reverse_lazy(
            'users:profile', kwargs={'username': self.object.username})


@login_required
def logout_view(request):
    logout(request)
    # return redirect('templates/logged_out.html')
    return render(request, 'registration/logged_out.html', {})


@login_required
def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj
    }
    return render(request, 'users/profile.html', context=context)


@login_required
def edit_profile(request, username):
    instance = get_object_or_404(User, username=username)
    if instance.id != request.user.id:
        raise PermissionDenied
    form = CustomUserChangeForm(request.POST or None,
                                files=request.FILES or None,
                                instance=instance)
    context = {
        'form': form
    }
    if form.is_valid():
        form.save()
    return render(request, 'users/user.html', context=context)
