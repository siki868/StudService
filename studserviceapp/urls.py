from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('timetable/<str:username>', views.timetableforuser, name='timetableforuser'),
    path('nastavnici', views.nastavnici, name='nastavnici'),
    path('unos_obavestenja/<str:user>', views.unos_obavestenja_form, name='unos_obavestenja'),
    path('save_obavestenje', views.save_obavestenje, name='save_obavestenje'),
    path('unos_semestra<str:user>', views.unos_semestra_form, name='unos_semestra'),
    path('save_semestar', views.save_semestar, name='save_semestar'),
    path('unos_izborne_grupe/<str:user>', views.unos_izborne_grupe_form, name='unos_izborne_grupe'),
    path('save_izborne_grupe', views.save_izborne_grupe, name='save_izborne_grupe'),
    path('izmena_izborne_grupe/<str:user>/<str:grupa>', views.izmena_izborne_grupe, name='izmena_izborne_grupe'),
    path('save_izmena_izborne_grupe', views.save_izmene_izborne_grupe, name='save_izmena_izborne_grupe'),
    path('izbor_grupe/<str:user>', views.izbor_grupe, name="izbor_grupe"),
    path('save_izbor_grupe', views.save_izbor_grupe, name='save_izbor_grupe'),
    path('izborne_grupe', views.izborne_grupe, name='izborne_grupe'),
    path('clanovi_grupe/<str:grupa>', views.clanovi_grupe, name='clanovi_grupe'),
    path('salji_mail/<str:username>', views.salji_mail_form, name='salji_mail'),
    path('salji_mail_save', views.salji_mail_save,name='salji_mail_save'),
    path('<str:username>', views.pregled, name='pregled'),
    path('<str:username>/dodaj', views.dodaj_sliku, name='dodaj_sliku'),
    path('<str:username>/sacuvaj_sliku', views.save_dodaj_sliku, name='save_dodaj_sliku'),
    path('grupa/<str:oznaka>', views.prikaz_grupe, name='prikaz_grupe')
]