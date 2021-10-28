from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView
from musicplayer import settings

from accounts.forms import CustomUserCreationForm
from accounts.models import User
from accounts.tokens import generate_token


class SignupView(CreateView):
    model = User
    template_name = "accounts/signup.html"
    form_class = CustomUserCreationForm
    success_url = "/"

    def form_valid(self, form):
        to_return = super().form_valid(form)
        email = self.object
        current_site = get_current_site(self.request)
        email_subject = "Confirm your Email"
        message2 = render_to_string('email_confirmation.html', {
            'name': email,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
            'token': generate_token.make_token(email)
        })
        email1 = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [email],
        )
        email1.fail_silently = True
        email1.send()

        return to_return


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        #messages.success(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        return render(request, 'accounts/email_confirmation.html')
