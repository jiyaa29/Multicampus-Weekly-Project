from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증

            if user is not None:
                login(request, user)  # 로그인
                #return redirect('index')

                # 로그인 된 후 webtoonitda main page로 이동
                return render(request, 'webtoonitda/index.html')
            else:
                # Return an 'invalid login' error message.
                return redirect('index')
                # return render(request, 'common/login.html')

    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


def page_not_found(request, exception):
    return render(request, 'common/404.html', {})
