import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studservice.settings")
import django
django.setup()
from studserviceapp.send_email import *
from studserviceapp.models import *
from studserviceapp.formater import *

import_timetable_from_csv('rasporedCSV.csv')
grupa = Grupa.objects.get(oznaka_grupe='303')
nal_nbadnjarevic = Nalog(username='nbadnjarevic16', uloga='student')
nal_nbadnjarevic.save()
nal_ndimitrijevic = Nalog(username='ndimitrijevic16', uloga='student')
nal_ndimitrijevic.save()
stud_nbadnjarevic = Student(
    ime='Nemanja',
    prezime='Badnjarevic',
    broj_indeksa='34',
    godina_upisa='2016',
    smer='RN',
    nalog=nal_nbadnjarevic)
stud_nbadnjarevic.save()
stud_nbadnjarevic.grupa.add(grupa)
stud_ndimitrijevic = Student(
    ime='Nikola',
    prezime='Dimitrijevic',
    broj_indeksa='47',
    godina_upisa='2016',
    smer='RN',
    nalog=nal_ndimitrijevic)
stud_ndimitrijevic.save()
stud_ndimitrijevic.grupa.add(grupa)
nal_administrator = Nalog(username='administrator', uloga='administrator')
nal_administrator.save()

import_kol_from_csv('kol1.csv')

emails = ['dzoni868@gmail.com', 'dzoni886@gmail.com']
subject = 'Test'
content = 'Test bez attachmenta'
salji_mailove(emails, subject, content)