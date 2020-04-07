from __future__ import unicode_literals

from django.db import models

from phonenumbers.phonenumberutil import PhoneNumberType


# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    iata = models.CharField(max_length=2)
    code = models.CharField(max_length=4, db_index=True)
    mobile_code = models.CharField(max_length=2, blank=True)
    trunk_prefix = models.CharField(max_length=3, blank=True, default='0')

    def __str__(self):
        return self.name


class AreaCode(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, db_index=True)
    code = models.CharField(max_length=4, db_index=True)
    name = models.CharField(max_length=100)


class NumGeoAr(models.Model):
    operador = models.CharField(max_length=100)
    servicio = models.CharField(max_length=20)
    modalidad = models.CharField(max_length=20)
    localidad = models.CharField(max_length=50)
    indicativo = models.CharField(max_length=10, db_index=True)
    bloque = models.CharField(max_length=5, db_index=True)
    resolucion = models.CharField(max_length=20)
    fecha = models.CharField(max_length=20)


class NumGeoMx(models.Model):
    clave_censal = models.CharField(max_length=20)
    poblacion = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    estado = models.CharField(max_length=10)
    presuscripcion = models.CharField(max_length=10)
    region = models.CharField(max_length=10)
    asl = models.CharField(max_length=10)
    nir = models.CharField(max_length=10, db_index=True)
    serie = models.CharField(max_length=10, db_index=True)
    numeracion_inicial = models.CharField(max_length=10, db_index=True)
    numeracion_final = models.CharField(max_length=10, db_index=True)
    ocupacion = models.CharField(max_length=10)
    tipo_red = models.CharField(max_length=20)
    modalidad = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=100)
    fecha_asignacion = models.CharField(max_length=10)
    fecha_consolidacion = models.CharField(max_length=10)
    fecha_migracion = models.CharField(max_length=10)
    nir_anterior = models.CharField(max_length=10)

    def __unicode__(self):
        return u'Nir: ' + self.nir + u' - Serie: ' + self.serie + u' - Numeracion Inicial: ' + self.numeracion_inicial + u' - Numeracion Final: ' + self.numeracion_final

    def __str__(self):
        return u'Nir: ' + self.nir + u' - Serie: ' + self.serie + u' - Numeracion Inicial: ' + self.numeracion_inicial + u' - Numeracion Final: ' + self.numeracion_final
