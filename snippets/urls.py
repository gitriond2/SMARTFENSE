from django.urls import path
from . import views

urlpatterns = [
    # Página de inicio
    path("", views.Index.as_view(), name="index"),

    # Login y Logout
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.LogoutViewCustom.as_view(), name="logout"),

    # Snippets por lenguaje
    path(
        "snippets/lang/<slug:language>/", views.SnippetsByLanguage.as_view(),name="language",
    ),

    # Snippets de usuario
    path(
        "snippets/user/<slug:username>/", views.UserSnippets.as_view(), name="user_snippets",
    ),

    # Detalles, creación, edición y eliminación de snippets
    path("snippets/<int:id>/", views.SnippetDetails.as_view(), name="snippet_detail"),
    path("snippets/add/", views.SnippetAdd.as_view(), name="snippet_add"),
    path("snippets/<int:id>/edit/", views.SnippetEdit.as_view(), name="snippet_edit"),
    path("snippets/<int:id>/delete/", views.SnippetDelete.as_view(), name="snippet_delete"),
    path("profile/", views.Profile.as_view(), name="profile"),
    path("snippet/<int:id>/", views.SnippetDetails.as_view(), name="snippet"),
    path("snippets/user/<str:username>/", views.UserSnippets.as_view(), name="user_snippets"),
    
]


