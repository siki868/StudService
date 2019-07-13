import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from studserviceapp.models import *
# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def izborne_grupe(request):
    izborne_grupe = IzbornaGrupa.objects.all()
    context = { 'izborne_grupe' : izborne_grupe }
    template = loader.get_template('izborne_grupe.html')
    return HttpResponse(template.render(context, request))

def clanovi_grupe(request, grupa):
    try:
        izborna_grupa = IzbornaGrupa.objects.get(oznaka_grupe=grupa)
        izbor_grupe = IzborGrupe.objects.filter(izabrana_grupa=izborna_grupa)
        studenti = []
        for stud in izbor_grupe:
            studenti.append(stud.student)
        context = { 'studenti' : studenti }
        template = loader.get_template('clanovi_grupe.html')
        return HttpResponse(template.render(context, request))
    except IzbornaGrupa.DoesNotExist:
        return HttpResponse('<h1>Ta grupa ne postoji</h1>')

def nastavnici(request):
    qs = Nastavnik.objects.all()
    context = { 'nastavnici' : qs}
    template = loader.get_template('nastavnici.html')
    return HttpResponse(template.render(context, request))

def unos_semestra_form(request, user):
    try:
        n = Nalog.objects.get(username = user)
        if n.uloga =='administrator':
            context = {'nalog':n}
            template = loader.get_template('unos_semestra.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse('<h1>Korisnik mora biti administrator</h1>')
    except Nalog.DoesNotExist:
        return HttpResponse('<h1>Username '+ user+' not found</h1>')

def save_semestar(request):
    vrsta = request.POST['vrsta']
    sgp = request.POST['skolska_godina_pocetak']
    sgk = request.POST['skolska_godina_kraj']
    semestar = Semestar(vrsta=vrsta,skolska_godina_pocetak=sgp,skolska_godina_kraj=sgk)
    semestar.save()
    return HttpResponse('<h1>Semestar sačuvano</h1>')

def izbor_grupe(request, user):
    try:
        n = Nalog.objects.get(username = user)
        if n.uloga =='student':
            semestri = Semestar.objects.all()
            predmeti = Predmet.objects.all()
            grupe = IzbornaGrupa.objects.all()
            s = Student.objects.get(nalog=n)
            semestar = Semestar.objects.latest('skolska_godina_kraj')
            try:
                izbor_grupe = IzborGrupe.objects.get(student=s)
            except IzborGrupe.DoesNotExist:
                context = {'student':s, 'grupe':grupe, 'predmeti':predmeti,'semestar':semestar}
                template = loader.get_template('izbor_grupe.html')
                return HttpResponse(template.render(context, request))
            return HttpResponse('<h1>Korisnik je vec izabrao grupu')
        else:
            return HttpResponse('<h1>Korisnik mora biti student</h1>')
    except Nalog.DoesNotExist:
        return HttpResponse('<h1>Username '+ user+' not found</h1>')

def save_izbor_grupe(request):
    ostvarenoESPB = request.POST['ostvarenoESPB']
    upisujeESPB = request.POST['upisujeESPB']
    broj_polozenih_ispita = request.POST['broj_polozenih_ispita']
    upisuje_semestar = request.POST['upisuje_semestar']
    prvi_put_upisuje_semestar = request.POST.get('prvi_put_upisuje_semestar', False)
    nacin_placanja = request.POST['nacin_placanja']
    nepolozeni_predmeti = request.POST.getlist('nepolozeni_predmeti')
    ime = request.POST['ime']
    prezime = request.POST['prezime']
    student = Student.objects.get(ime=ime, prezime=prezime)
    izabrana_grupa = request.POST['izabrana_grupa']
    if prvi_put_upisuje_semestar == 'on':
        prvi_put_upisuje_semestar = True
    izbor_grupe = IzborGrupe(
        ostvarenoESPB = ostvarenoESPB,
        upisujeESPB = upisujeESPB,
        broj_polozenih_ispita = broj_polozenih_ispita,
        upisuje_semestar = upisuje_semestar,
        prvi_put_upisuje_semestar = prvi_put_upisuje_semestar,
        nacin_placanja = nacin_placanja,
        student = student,
        izabrana_grupa = IzbornaGrupa.objects.get(oznaka_grupe=izabrana_grupa),
        upisan = True,
    )
    izbor_grupe.save()
    for p in nepolozeni_predmeti:
        pred = Predmet.objects.get(naziv=p)
        izbor_grupe.nepolozeni_predmeti.add(pred)
    return HttpResponse('<h1>Izabrana grupa</h1>')

def unos_izborne_grupe_form(request, user):
    try:
        n = Nalog.objects.get(username = user)
        if n.uloga =='administrator':
            semestri = Semestar.objects.all()
            predmeti = Predmet.objects.all()
            context = {'nalog':n, 'semestri':semestri, 'predmeti':predmeti}
            template = loader.get_template('unos_izborne_grupe.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse('<h1>Korisnik mora biti administrator</h1>')
    except Nalog.DoesNotExist:
        return HttpResponse('<h1>Username '+ user+' not found</h1>')

def izmena_izborne_grupe(request, user, grupa):
    try:
        n = Nalog.objects.get(username = user)
        if n.uloga =='administrator':
            semestri = Semestar.objects.all()
            predmeti = Predmet.objects.all()
            izborna_grupa = IzbornaGrupa.objects.get(oznaka_grupe=grupa)
            context = {'nalog':n, 'semestri':semestri, 'predmeti':predmeti, 'grupa':izborna_grupa}
            template = loader.get_template('izmena_izborne_grupe.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse('<h1>Korisnik mora biti administrator</h1>')
    except Nalog.DoesNotExist:
        return HttpResponse('<h1>Username '+ user+' not found</h1>')

def save_izborne_grupe(request):
    oznaka_grupe = request.POST['oznaka_grupe']
    oznaka_semestra = int(request.POST['oznaka_semestra'])
    kapacitet = int(request.POST['kapacitet'])
    smer = request.POST['smer']
    aktivna = request.POST.get('aktivna', False)
    semestar = request.POST['semestar']
    predmeti = request.POST.getlist('predmeti')
    semestar_args = semestar.split('/')
    if aktivna == 'on':
        aktivna = True
    izborna_grupa = IzbornaGrupa(
        oznaka_grupe=oznaka_grupe,
        oznaka_semestra=oznaka_semestra,
        kapacitet=kapacitet,
        smer=smer,
        aktivna=aktivna,
        za_semestar=Semestar.objects.get(skolska_godina_kraj=semestar_args[1],skolska_godina_pocetak=semestar_args[0]),
        )
    izborna_grupa.save()
    for p in predmeti:
        pred = Predmet.objects.get(naziv=p)
        izborna_grupa.predmeti.add(pred)
    return HttpResponse('<h1>Izborna grupa sačuvana</h1>')

def save_izmene_izborne_grupe(request):
    oznaka_grupe = request.POST['oznaka_grupe']
    kapacitet = int(request.POST['kapacitet'])
    aktivna = request.POST.get('aktivna', False)
    if aktivna == 'on':
        aktivna = True
    IzbornaGrupa.objects.filter(oznaka_grupe=oznaka_grupe).update(kapacitet=kapacitet,aktivna=aktivna)
    return HttpResponse('<h1>Izborna grupa izmenjena</h1>')


def unos_obavestenja_form(request,user):
    try:
        n = Nalog.objects.get(username = user)
        if n.uloga=='sekretar' or n.uloga=='administrator':
            context = {'nalog':n}
            template = loader.get_template('unos_obavestenja.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse('<h1>Korisnik mora biti sekretar ili administrator</h1>')
    except Nalog.DoesNotExist:
        return HttpResponse('<h1>Username '+ user+' not found</h1>')

def save_obavestenje(request):
    tekst = request.POST['tekst']
    postavio = Nalog.objects.get(username=request.POST['postavio'])
    obavestenje = Obavestenje(tekst=tekst,postavio=postavio,datum_postavljanja=datetime.datetime.now())
    obavestenje.save()
    return HttpResponse('<h1>Obavestenje sačuvano</h1>')

def timetableforuser(request, username):
    try:
        nalog = Nalog.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404("Ne postoji nalog sa username-om  %s." % username)
    if nalog.uloga == 'student':
        student = Student.objects.get(nalog=nalog)
        grupe = []
        for g in student.grupa.all():
            grupe.append(g)
        try:
            termini = Termin.objects.filter(grupe=grupe[0]).all()
        except ObjectDoesNotExist:
            return HttpResponse("Grupa studenta %s nema termina")
        template = loader.get_template('timetable.html')
        context = {
            'termini': termini,
        }
        return HttpResponse(template.render(context, request))
    elif nalog.uloga == 'nastavnik':
        nalog = Nalog.objects.get(username=username)
        nastavnik = Nastavnik.objects.get(nalog=nalog)
        try:
            termini = Termin.objects.filter(nastavnik=nastavnik).all()
        except ObjectDoesNotExist:
            return HttpResponse("Nastavnik %s nema termina")
        template = loader.get_template('timetable.html')
        context = {
            'termini': termini,
        }
        return HttpResponse(template.render(context, request))


def salji_mail_form(request, username):
    try:
        nalog = Nalog.objects.get(username=username)
        if(nalog.uloga == 'nastavnik'):
            email = username + '@raf.rs'
            nastavnik = Nastavnik.objects.get(nalog=nalog)
            predmeti = nastavnik.predmet.all()
            context = {'nastavnik': nastavnik, 'predmeti': predmeti, 'email':email}
            template = loader.get_template('salji_mail.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse('<h1>Dostupno samo profesorima, sekretaru i administratoru</h1>')
    except ObjectDoesNotExist:
        raise Http404('Ne postoji nalog sa username-om  %s.' % username)
    
def salji_mail_save(request):
    #ovde treba iz send_email da salje svima koji su izabrani
    f = request.POST['file']
    return HttpResponse(f'<h1>{f}</h1>')

def pregled(request, username):
    try:
        nalog = Nalog.objects.get(username=username)
        if(nalog.uloga == 'student'):
            student = Student.objects.get(nalog=nalog)
            context = {'student': student, 'nalog': nalog}
            template = loader.get_template('pregled.html')
            return HttpResponse(template.render(context, request))
        elif(nalog.uloga == 'nastavnik'):
            nastavnik = Nastavnik.objects.get(nalog=nalog)
            termini = Termin.objects.filter(nastavnik=nastavnik)
            rezultat = dict()
            for t in termini:
                predmet = t.predmet.naziv
                rezultat.setdefault(predmet, [])
                for x in t.grupe.all():
                    grupa = x.oznaka_grupe
                    rezultat[predmet].append(grupa)
            context = {'nalog': nalog,'rezultat':rezultat}
            template = loader.get_template('pregled.html')
            return HttpResponse(template.render(context, request))
            

    except ObjectDoesNotExist:
        raise Http404('Ne postoji nalog sa username-om  %s.' % username)

def dodaj_sliku(request, username):
    try:
        nalog = Nalog.objects.get(username=username)
        student = Student.objects.get(nalog=nalog)
        context = {'nalog':nalog, 'student':student}
        template = loader.get_template('dodaj_sliku.html')
        return HttpResponse(template.render(context, request))
    except ObjectDoesNotExist:
        raise Http404('Ne postoji nalog sa username-om  %s.' % username)

from django.core.files.storage import FileSystemStorage
def save_dodaj_sliku(request, username):
    nalog = Nalog.objects.get(username=username)
    student = Student.objects.get(nalog=nalog)
    slika = request.FILES['pic']
    fs = FileSystemStorage()
    filename = fs.save(slika.name, slika)
    uploaded_file_url = fs.url(filename)
    student.slika = slika.name
    student.save()
    return HttpResponse('<h1>Slika sačuvana</h1>')

def prikaz_grupe(request, oznaka):
    try:
        grupa = Grupa.objects.get(oznaka_grupe=oznaka)
        studenti = Student.objects.filter(grupa=grupa)
        context = {'studenti':studenti}
        template = loader.get_template('clanovi_grupe.html')
        return HttpResponse(template.render(context, request))
    except ObjectDoesNotExist:
        raise Http404('Ne postoji grupa sa oznakom  %s.' % oznaka)