from django.db import models
from django.core.exceptions import ValidationError


class Andraikitra(models.Model):
    andraikitra = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.andraikitra

    class Meta:
        verbose_name_plural = 'Andraikitra'

    def save(self, *args, **kwargs):
        self.andraikitra = self.andraikitra.strip()
        super().save(*args, **kwargs)


class Apv(models.Model):
    apv = models.IntegerField(primary_key=True)
    mpiaro = models.CharField(max_length=50)
    fankalazana = models.DateField()

    def __str__(self):
        return f"{self.apv}"

    class Meta:
        verbose_name_plural = 'Apv'

    def save(self, *args, **kwargs):
        self.mpiaro = self.mpiaro.strip()
        super().save(*args, **kwargs)


class Fikambanana(models.Model):
    FARITRA = 'FAR'
    FM = 'FIK'
    VAOMIERA = 'VAO'
    SOKAJY = [
        (FARITRA, 'Faritra'),
        (FM, 'Fikambanana Masina'),
        (VAOMIERA, "Vaomieran'asa")
    ]
    sokajy = models.CharField(max_length=3, choices=SOKAJY)
    fikambanana = models.CharField(max_length=50, unique=True)
    mpiaro = models.CharField(max_length=50)
    fankalazana = models.DateField()

    def __str__(self):
        return f"{self.fikambanana}"

    class Meta:
        verbose_name_plural = 'Fikambanana'

    def save(self, *args, **kwargs):
        self.fikambanana = self.fikambanana.upper().strip()
        self.mpiaro = self.mpiaro.strip()
        super().save(*args, **kwargs)


class Kristianina(models.Model):
    anarana = models.CharField(max_length=100, unique=True)
    apv = models.ForeignKey(Apv, on_delete=models.PROTECT)
    nahaterahana = models.CharField(max_length=20, default='', blank=True)
    nahatongavana = models.CharField(max_length=20, default='', blank=True)
    batemy = models.CharField(max_length=20, default='', blank=True)
    eokaristia = models.CharField(max_length=20, default='', blank=True)
    fankaherezana = models.CharField(max_length=20, default='', blank=True)
    mariazy = models.CharField(max_length=20, default='', blank=True)
    asa = models.CharField(max_length=50, default='', blank=True)
    fanamarihana = models.TextField(default='', blank=True)
    tel = models.CharField(max_length=50, blank=True, default='')
    mail = models.EmailField(blank=True, default='')

    class Meta:
        verbose_name_plural = 'Kristianina'

    def __str__(self):
        return f"{self.anarana}"

    def save(self, *args, **kwargs):
        self.anarana = self.anarana.strip()
        self.nahaterahana = self.nahaterahana.strip()
        self.nahatongavana = self.nahatongavana.strip()
        self.batemy = self.batemy.strip()
        self.eokaristia = self.eokaristia.strip()
        self.fankaherezana = self.fankaherezana.strip()
        self.mariazy = self.mariazy.strip()
        self.asa = self.asa.strip()
        self.tel = self.tel.strip()
        super().save(*args, **kwargs)


class Lohampianakaviana(models.Model):
    kristianina = models.OneToOneField(Kristianina, on_delete=models.PROTECT,
                                       primary_key=True)
    karatra = models.CharField(max_length=20, blank=True, default='')
    adiresy = models.CharField(max_length=100, blank=True, default='')
    fanamarihana = models.TextField(blank=True, default='')
    isaina = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Lohampianakaviana'

    def __str__(self):
        return f"{self.kristianina}"

    def save(self, *args, **kwargs):
        self.karatra = self.karatra.strip()
        self.adiresy = self.adiresy.strip()
        t = Tokantrano.objects.filter(pk=self.kristianina)
        if t.exists():
            t = t[0]
            if t.lohampianakaviana_id != self.kristianina_id:
                raise ValidationError(
                    f"Efa ao anaty tokantrano {self.kristianina}."
                )
        super().save(*args, **kwargs)
        t = Tokantrano(kristianina_id=self.kristianina_id, laharana=1,
                       lohampianakaviana_id=self.kristianina_id)
        t.save()


class Tokantrano(models.Model):
    kristianina = models.OneToOneField(Kristianina, on_delete=models.PROTECT,
                                       primary_key=True)
    lohampianakaviana = models.ForeignKey(Lohampianakaviana,
                                          on_delete=models.PROTECT)
    laharana = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.kristianina}"

    class Meta:
        verbose_name_plural = 'Tokantrano'

    def save(self, *args, **kwargs):
        if Lohampianakaviana.objects.filter(pk=self.kristianina).exists():
            if self.kristianina.id != self.lohampianakaviana.kristianina_id:
                raise ValidationError(
                    f"Efa lohampianakaviana {self.kristianina}"
                )
        if self.kristianina.apv.apv != \
                self.lohampianakaviana.kristianina.apv.apv:
            raise ValidationError('Tsy mitovy ny APV')
        super().save(*args, **kwargs)


class Bordereau(models.Model):
    lohampianakaviana = models.ForeignKey(Lohampianakaviana,
                                          on_delete=models.PROTECT)
    date = models.DateField()
    numero = models.IntegerField()
    ligne = models.IntegerField()
    verse_par = models.CharField(max_length=50)
    recu_par = models.CharField(max_length=50)
    taona = models.IntegerField()
    hasina = models.IntegerField()
    seminera = models.IntegerField()
    diosezy = models.IntegerField()
    marina = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['numero', 'ligne'],
                                    name='bordereau')
        ]
        verbose_name_plural = 'Bordereaux'

    def save(self, *args, **kwargs):
        self.verse_par = self.verse_par.strip()
        self.recu_par = self.recu_par.strip()
        b = Bordereau.objects.filter(pk=self.id)
        if b.exists():
            b = b[0]
            if b.marina != 0:
                raise ValidationError(f"{b} : tsy azo ovaina intsony")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero}-{self.ligne}"


class Mpikambana(models.Model):
    fikambanana = models.ForeignKey(Fikambanana, on_delete=models.PROTECT)
    kristianina = models.ForeignKey(Kristianina, on_delete=models.PROTECT)
    andraikitra = models.ForeignKey(Andraikitra, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.kristianina}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fikambanana', 'kristianina'],
                                    name='mpikambana')
        ]
        verbose_name_plural = 'Mpikambana'
