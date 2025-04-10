from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from snippets.forms import SnippetForm  
from django.shortcuts import get_object_or_404
from snippets.models import Snippet
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import logout
from django.db import models



class SnippetAdd(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = SnippetForm()
        return render(request, "snippets/snippet_add.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return HttpResponseRedirect(reverse("snippet_detail", kwargs={"id": snippet.id}))
        return self.get(request)

class SnippetEdit(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=self.kwargs["id"], user=request.user)
        form = SnippetForm(instance=snippet)
        return render(request, "snippets/snippet_add.html", {"form": form, "action": "Editar"})

    def post(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=self.kwargs["id"], user=request.user)
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("snippet_detail", kwargs={"id": snippet.id}))
        return render(request, "snippets/snippet_add.html", {"form": form, "action": "Editar"})

class SnippetDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=self.kwargs["id"], user=request.user)
        return render(request, "snippets/snippet_confirm_delete.html", {"snippet": snippet})

    def post(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=self.kwargs["id"], user=request.user)
        snippet.delete()
        return HttpResponseRedirect(reverse("index"))


class UserSnippets(View):
    def get(self, request, username):
        user_snippets = Snippet.objects.filter(user__username=username)
        if request.user.username == username:
            snippets = user_snippets
        else:
            snippets = user_snippets.filter(public=True)
        return render(request, "snippets/user_snippets.html", {"snippets": snippets, "snippetUsername": username})
    
    
class SnippetDetails(View):
    def get(self, request, *args, **kwargs):
        snippet_id = self.kwargs["id"]
        snippet = get_object_or_404(Snippet, id=snippet_id)

        # Si el snippet es privado y no pertenece al usuario actual, deniega acceso
        if not snippet.public and snippet.user != request.user:
            return render(request, "403.html")  # Puedes usar un template simple o redirigir.
        return render(
            request, "snippets/snippet.html", {"snippet": snippet}
        )


class SnippetsByLanguage(View):
    def get(self, request, *args, **kwargs):
        language = self.kwargs["language"]
        # TODO: Fetch snippets based on language
        return render(request, "index.html", {"snippets": []})  # Placeholder


class Login(LoginView):
    template_name = "snippets/login.html"

class LogoutViewCustom(View):
    def get(self, request, *args, **kwargs):
        # Cierra sesión del usuario
        if request.user.is_authenticated:  # Asegurarse de que el usuario está autenticado
            logout(request)
            messages.success(request, "Has cerrado sesión correctamente.")  # Envía el mensaje solo una vez
        return redirect("/login/")  # Redirige al login


class Index(View):
    def get(self, request):
        if request.user.is_authenticated:
            snippets = Snippet.objects.all()
        else:
            snippets = Snippet.objects.filter(public=True)
        return render(request, "index.html", {"snippets": snippets})
    

class Profile(LoginRequiredMixin, View):
    def get(self, request):
        user_snippets = Snippet.objects.filter(user=request.user)
        return render(
            request,
            "snippets/profile.html",
            {"user_snippets": user_snippets, "user": request.user},
        )


