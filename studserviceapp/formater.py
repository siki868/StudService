import csv
from django.utils import timezone
from .models import *
from datetime import datetime

def import_timetable_from_csv(file_path):
    """Otvara csv fajl i parsira podatke za svaki predmet

    Args:
        file_path: Putanja csv fajla koji parsiramo


    """
    # Univerzalni semestar za trenutno unosenje
    if not Semestar.objects.filter(
            vrsta='neparni',
            skolska_godina_pocetak=2018,
            skolska_godina_kraj=2019
        ).exists():
        sem = Semestar(vrsta='neparni', skolska_godina_pocetak=2018, skolska_godina_kraj=2019)
        sem.save()
    else:
        sem = Semestar.objects.get(
            vrsta='neparni',
            skolska_godina_pocetak=2018,
            skolska_godina_kraj=2019
            )

    # Otvara fajl i za svaki predmet poziva funkciju formatiraj()
    with open(file_path, encoding='utf-8') as csvfile:
        raspored_csv = csv.reader(csvfile, delimiter=';')
        raspored_csv = list(raspored_csv)
        vrste = parsiraj_vrste(raspored_csv[1])
        sve = [raspored_csv[i] for i in range(2, len(raspored_csv))]
        predmeti = []
        predmet = []
        for red in sve:
            if not red:
                predmeti.append(predmet)
                predmet = []
            else:
                predmet.append(red)
        for p in predmeti:
            formatiraj(p, vrste)
            


def formatiraj(predmet, vrste):
    """Parsuje sve termine za odredjen predmet i poziva dodaj_u_bazu()

    Args:
        predmet: Predmet koji trenutno parsiramo

    """
    ime = predmet[0][0]
    pred = Predmet(naziv=ime)
    pred.save()
    pred = Predmet.objects.get(naziv=ime)
    svi = vrati_listu_predavaca(predmet[2:], vrste)
    for p in svi:
        dodaj_u_bazu(pred, p[0], p[1], p[2].split(', '), p[4], p[5], p[6], p[7])

   
#predavanja-1 praktikum-9 vezbe-17 25-pred i vez
def vrati_listu_predavaca(blok, vrste):
    pred = []
    svi_pred = []
    for linija in blok:
        p = 0
        i = 0
        while i < len(linija):
            if(linija[i] == ''):
                p+=1
                i+=1
            else:
                for j in range (i, i+7):
                    pred.append(linija[j])
                pred.append(vrste.get(p))
                svi_pred.append(pred)
                p = 0
                pred = []
                i += 7
    return svi_pred



def parsiraj_vrste(linija):
    ret = dict()
    p = 0
    for i in range(0, len(linija)):
        if(linija[i] == ''):
            p+=1
        else:
            ret.update({p:linija[i]})
            p+=1
    return ret



def dodaj_u_bazu(pred, ime_profesora, sifra_profesora, grupe, dan, satnica, ucionica, tip_n):
    """Dodaje u bazu parsovane informacije

    Args:
        pred: Objekat po modelu za tip Predmet
        ime_profesora:  Ime i Prezime profesora zajedno
        sifra_profesora: Sifra profesora(da bi razlikovali da li su vezbe ili predavanja)
        grupe: Lista grupa koje odgovaraju datom terminu
        dan: Dan kada se termin odrzava
        satnica: Satnica odrzavanja termina (npr. 13:15-15)
        ucionica: Ucionica u kojoj se termin odrzava

    """

    '''
    ime_profesora predstavlja Ime i Prezime profesora zajedno, a nama su potrebni kao
    odvojeni podaci. Takodje su nam potrebni da bi napravili username.
    if i else su zato sto neki profesori u csv fajl-u nemaju ime, samo prezime.
    '''
    ime_split = ime_profesora.split(' ')
    prez_prof = ime_split[0]
    if len(ime_split) == 2:
        ime_prof = ime_split[1]
        username = ime_prof[0].lower()  + prez_prof.lower()
    elif len(ime_split) == 3:
        prez_prof = ime_split[0] + " " + ime_split[1]
        ime_prof = ime_split[2]
        if ime_prof == '':
            username = prez_prof.lower()
        else:
            username = (ime_split[2][0] + ime_split[0] + ime_split[1]).lower()       
    predmeti = []
    predmeti.append(pred)
    sem = Semestar.objects.get(
        vrsta='neparni',
        skolska_godina_pocetak=2018,
        skolska_godina_kraj=2019
        )
    #Ako nastavnik vec nije unesen u bazu, onda moramo da ga dodamo
    if not Nastavnik.objects.filter(ime=ime_prof, prezime=prez_prof).exists():
        uloga = 'nastavnik'
        #Dolazi do preklapanja kod username-ova, pa se na nove dodaje broj
        if not Nalog.objects.filter(username=username).exists():
            nal = Nalog(username=username, uloga=uloga)
            nal.save()
        else:
            username = username + str(Nalog.objects.filter(username=username).count())
            nal = Nalog(username=username, uloga=uloga)
            nal.save()
        prof = Nastavnik(ime=ime_prof, prezime=prez_prof, nalog=nal)
        prof.save()
        prof.predmet.add(pred)
    else:
        nal = Nalog.objects.get(username=username)
        nas = Nastavnik.objects.get(nalog=nal)
        nas.predmet.add(pred)

    prof = Nastavnik.objects.get(nalog=nal)
    poc_kraj = satnica.split('-')
    ras_nas = RasporedNastave(datum_unosa=timezone.now(), semestar=sem)
    ras_nas.save()
    term = Termin(
        oznaka_ucionice=ucionica,
        pocetak=poc_kraj[0],
        zavrsetak=poc_kraj[1]+':00',
        dan=dan,
        tip_nastave=tip_n,
        nastavnik=prof,
        predmet=pred,
        raspored=ras_nas
        )
    term.save()
    # Svaki termin ima vise grupa, te ovo dodaje odgovarajuce u termin
    for grupa in grupe:
        # Ako grupa ne postoji potrebno je napraviti novu
        if not Grupa.objects.filter(oznaka_grupe=grupa).exists():
            grupa_za_termin = Grupa(oznaka_grupe=grupa, semestar=sem)
            grupa_za_termin.save()
            grupa_za_termin = Grupa.objects.get(oznaka_grupe=grupa)
            term.grupe.add(grupa_za_termin)
        else:
            grupa_za_termin = Grupa.objects.get(oznaka_grupe=grupa)
            term.grupe.add(grupa_za_termin)
    



def import_kol_from_csv(file_path):
    termini = []
    cuvaj = False
    rp = RasporedPolaganja(ispitni_rok='Ne znam?', kolokvijumska_nedelja='prva valjda')
    rp.save()
    with open(file_path, encoding='utf-8') as csvfile:
        raspored_csv = csv.reader(csvfile, delimiter=',')
        raspored_csv = list(raspored_csv)
        
        d = dict(enumerate(raspored_csv[0]))
        print(d)
        for linija in raspored_csv[1:]:
            predmet = linija[0]
            profesori = linija[3]
            ucionice = linija[4]
            vreme = linija[5]
            dan = linija[6]
            datum = linija[7]
            proveri(predmet, profesori, ucionice, vreme, dan, datum, rp, termini)

    #ovde treba da pita da li hoce da popravi file ili da radi preko formi
    #ako hoce preko formi cuvaju se svi validni rasporedi, to je cuvaj = True

    if(cuvaj):
        for t in termini:
            t.save()
    else:
        #prave se forme
        pass

def proveri(predmet, profesori, ucionice, vreme, dan, datum, rp, termini):
    profa = None
    pred = None
    profesori = profesori.split(', ')
    for prof in profesori:
        if(len(prof.split(' ')) > 3):
            #forma
            print('Profesora ' + prof + ' nije moguce isparsirati.')
            pass
        else:
            auBrate = prof.split(' ')
            ime = auBrate[0]
            prezime = ''
            if(len(auBrate) == 2):
                prezime = auBrate[1]
            elif(len(auBrate) == 3):
                prezime = auBrate[1] + ' ' + auBrate[2]
            try:
                profa = Nastavnik.objects.get(ime=ime, prezime=prezime)
            except:
                #forma
                print(ime + ' '  + prezime + ' nije u bazi.')
                return 
            
    try:
        pred = Predmet.objects.get(naziv=predmet)
    except:
        print(predmet + ' ne postoji u bazi')
        return

    ucionice = ucionice.replace('"', '')
    ucionice = ucionice.replace('.', ',')

    poc_kraj = vreme.split('-')
    poc = poc_kraj[0] + ':00'
    kraj = poc_kraj[1] + ':00'

    datum += '2018'  #ovde treba da se nadje prava godina
    datum = datetime.strptime(datum, '%d.%m.%Y').date()

    if(pred is not None and profa is not None):
        tp = TerminPolaganja(ucionice=ucionice, pocetak=poc, zavrsetak=kraj, datum=datum, raspored_polaganja=rp, predmet=pred, nastavnik=profa)
        termini.append(tp)