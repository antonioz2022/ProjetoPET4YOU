from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = "pet4you"
urlpatterns = [
    path("", views.home, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register_view, name='register'),
    path("posting/", views.createPost, name="posting"),
    path("report_list/", views.list_reports, name="report_list"),
    path("report/<int:pet_id>/", views.add_report, name='report'),
    path("report_admin/<int:report_id>/", views.report_admin_view, name='report_admin'),
    path("list/", views.listPets, name= "list"),
    path("favorite/", views.listFavorites, name= "favorite"),
    path("edit/<int:pet_id>/", views.edit_post, name="edit_post"),
    path('favoritar_pet/<int:pet_id>/', views.favoritar_pet, name='favoritar_pet'),
    path('desfavoritar_pet/<int:pet_id>/', views.desfavoritar_pet, name='desfavoritar_pet'),
    path('listar_pets/', views.listar_pets, name='listar_pets'),
    path('delete/<int:pet_id>/', views.delete_post, name='delete_post'),
    path('api/create_admin/', views.create_admin_user, name='create_admin_user'),
    path('pets/<int:pet_id>/vaccine_card/', views.vaccine_card, name='vaccine_card'),
    path('pets/<int:pet_id>/vaccine_add/', views.vaccine_add, name='vaccine_add'),
    path('download_pet/<int:pet_id>/', views.download_pet, name='download_pet'),
    path("delete_as_user/<int:pet_id>/", views.delete_post_as_user, name="delete_post_as_user"),
    path('adopt/<int:pet_id>/', views.adopt_pet, name='adopt_pet'),



    
]