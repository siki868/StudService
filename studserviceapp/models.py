from django.db import models


class Semestar(models.Model):
    vrsta = models.CharField(max_length=20)  # parni/neparni
    skolska_godina_pocetak = models.IntegerField()  # primer 2018
    skolska_godina_kraj = models.IntegerField()  # primer 2019

    class Meta:
        verbose_name_plural = "Semestri"


class Grupa(models.Model):
    oznaka_grupe = models.CharField(max_length=10)
    smer = models.CharField(max_length=20, null=True)
    semestar = models.ForeignKey(Semestar, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.oznaka_grupe

    class Meta:
        verbose_name_plural = "Grupe"


class Nalog(models.Model):
    username = models.CharField(max_length=200)
    lozinka = models.CharField(max_length=100, null=True)  # google login, necemo koristiti password
    uloga = models.CharField(max_length=50)  # student, nastavnik, sekretar, administrator

    def __str__(self):
        return self.username + " " + self.uloga

    class Meta:
        verbose_name_plural = "Nalozi"


class Student(models.Model):
    ime = models.CharField(max_length=200)
    prezime = models.CharField(max_length=200)
    broj_indeksa = models.IntegerField()
    godina_upisa = models.IntegerField()
    smer = models.CharField(max_length=20)
    nalog = models.ForeignKey(Nalog, on_delete=models.CASCADE)
    grupa = models.ManyToManyField(Grupa)
    slika = models.ImageField(null=True)

    def __str__(self):
        return self.ime + " " + self.prezime

    class Meta:
        verbose_name_plural = "Studenti"

class Predmet(models.Model):
    naziv = models.CharField(max_length=200)
    espb = models.IntegerField(null=True)
    semestar_po_programu = models.IntegerField(null=True)  # redni broj semestra u kom se slusa predmet
    fond_predavanja = models.IntegerField(null=True)
    fond_vezbe = models.IntegerField(null=True)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name_plural = "Predmeti"

class Nastavnik(models.Model):
    ime = models.CharField(max_length=200)
    prezime = models.CharField(max_length=200)
    titula = models.CharField(max_length=20, null=True)
    zvanje = models.CharField(max_length=40, null=True)
    nalog = models.ForeignKey(Nalog, on_delete = models.CASCADE)
    predmet = models.ManyToManyField(Predmet)

    def __str__(self):
        return self.ime + " " + self.prezime

    class Meta:
        verbose_name_plural = "Nastavnici"


class RasporedNastave(models.Model):
    datum_unosa = models.DateTimeField()
    semestar = models.ForeignKey(Semestar, on_delete=models.PROTECT)
    class Meta:
        verbose_name_plural = "Raspored nastave"


class Termin(models.Model):
    oznaka_ucionice = models.CharField(max_length=50)
    pocetak = models.TimeField()
    zavrsetak = models.TimeField()
    dan = models.CharField(max_length=15)
    tip_nastave = models.CharField(max_length=25)  # predavanja, vezbe, praktikum
    nastavnik = models.ForeignKey(Nastavnik, on_delete=models.DO_NOTHING)
    predmet = models.ForeignKey(Predmet, on_delete=models.DO_NOTHING)
    grupe = models.ManyToManyField(Grupa)
    raspored = models.ForeignKey(RasporedNastave, on_delete=models.CASCADE)

    def __str__(self):
        return self.oznaka_ucionice + " " + self.dan

    class Meta:
        verbose_name_plural = "Termini"


class RasporedPolaganja(models.Model):
    ispitni_rok = models.CharField(max_length=50, null=True)
    kolokvijumska_nedelja = models.CharField(max_length=50, null=True)


class TerminPolaganja(models.Model):
    ucionice = models.CharField(max_length=100)
    pocetak = models.TimeField()
    zavrsetak = models.TimeField()
    datum = models.DateField()
    raspored_polaganja = models.ForeignKey(RasporedPolaganja, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmet, on_delete=models.DO_NOTHING)
    nastavnik = models.ForeignKey(Nastavnik, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Termini polaganja"

class IzbornaGrupa(models.Model):
    oznaka_grupe = models.CharField(max_length=20)
    oznaka_semestra = models.IntegerField()
    kapacitet = models.IntegerField()
    smer = models.CharField(max_length=20)
    aktivna = models.BooleanField()
    za_semestar = models.ForeignKey(Semestar, on_delete=models.DO_NOTHING)
    predmeti = models.ManyToManyField(Predmet)

    def __str__(self):
        return self.oznaka_grupe

    class Meta:
        verbose_name_plural = "Izborne grupe"


class IzborGrupe(models.Model):
    ostvarenoESPB = models.IntegerField()
    upisujeESPB = models.IntegerField()
    broj_polozenih_ispita = models.IntegerField()
    upisuje_semestar = models.IntegerField()  # redni broj semestra
    prvi_put_upisuje_semestar = models.BooleanField()
    nacin_placanja = models.CharField(max_length=30)
    nepolozeni_predmeti = models.ManyToManyField(Predmet)
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    izabrana_grupa = models.ForeignKey(IzbornaGrupa,on_delete=models.CASCADE)
    upisan = models.BooleanField()  # na pocetku staviti false

    class Meta:
        verbose_name_plural = "Izbori grupa"


class VazniDatumi(models.Model):
    kategorija = models.CharField(max_length=200) # kolokvijumske nedelje, ispitni rokovi, placanje skolarine na rate,...
    oznaka = models.CharField(max_length=200) # I, Jan, Feb. I rata, RAF Hackaton,...
    datum_od = models.DateField(null=True)
    datum_do = models.DateField(null=True)
    okvirno = models.CharField(max_length=200,null=True)
    skolska_godina = models.CharField(max_length=15)   # 2018/2019

    class Meta:
        verbose_name_plural = "Vazni datumi"


class Konsultacije(models.Model):
    nastavnik = models.ForeignKey(Nastavnik, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmet, on_delete=models.CASCADE,null=True)
    mesto = models.CharField(max_length=50)
    vreme_od = models.TimeField()
    vreme_do = models.TimeField()
    dan = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = "Konsultacije"


class Obavestenje(models.Model):
    postavio = models.ForeignKey(Nalog, on_delete=models.DO_NOTHING)
    datum_postavljanja = models.DateTimeField()
    tekst = models.CharField(max_length=1000)
    fajl = models.FileField()

    class Meta:
        verbose_name_plural = "Obavestenja"



class PripadaGrupi(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semestar = models.ForeignKey(Semestar, on_delete=models.CASCADE)
    grupa = models.ForeignKey(Grupa, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Pripada grupi"