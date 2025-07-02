from django.conf import settings
from django.db import models

class RegistroCarga(models.Model):
    """
    Representa un lote de importación de incidencias.
    Guarda quién y cuándo se realizó la carga.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Usuario que realizó la carga"
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que se creó la carga"
    )

    def __str__(self):
        return f"RegistroCarga #{self.id} por {self.usuario} el {self.creado_en:%Y-%m-%d %H:%M}"


class ViolenciaFamiliar(models.Model):
    id = models.AutoField(primary_key=True)

    id_doc_denuncia      = models.IntegerField()
    libro                = models.CharField(max_length=200)
    num_denuncia         = models.CharField(max_length=200)
    tipodenuncia         = models.CharField(max_length=200)
    situaciondenuncia    = models.CharField(max_length=200)
    tipo                 = models.CharField(max_length=200)
    subtipo              = models.CharField(max_length=300)
    modalidad            = models.CharField(max_length=200)

    fec_hecho_fecha      = models.DateField(null=True, blank=True)
    fec_hecho_hora       = models.TimeField(null=True, blank=True)

    dpto                 = models.CharField(max_length=200)
    prov                 = models.CharField(max_length=200)
    distrito             = models.CharField(max_length=200)
    tipovia              = models.CharField(max_length=200)
    ubicacion            = models.CharField(max_length=200)
    cuadra               = models.CharField(max_length=100, blank=True)
    dni                  = models.CharField(max_length=20)
    apellido_paterno     = models.CharField(max_length=200)
    apellido_materno     = models.CharField(max_length=200)
    nombre               = models.CharField(max_length=200)
    situacionpersona     = models.CharField(max_length=200)

    fec_nacimiento_fecha = models.DateField(null=True, blank=True)
    fec_nacimiento_hora  = models.TimeField(null=True, blank=True)

    edad                 = models.IntegerField(null=True, blank=True)
    sexo                 = models.CharField(max_length=50)
    estadocivil          = models.CharField(max_length=100)
    gradoinstruccion     = models.CharField(max_length=200, blank=True)
    ocupacion            = models.CharField(max_length=200, blank=True)
    pais_natal           = models.CharField(max_length=200)
    region               = models.CharField(max_length=200)
    descripcioncomisaria = models.CharField(max_length=300)

    fec_registro_fecha   = models.DateField(null=True, blank=True)
    fec_registro_hora    = models.TimeField(null=True, blank=True)

    xx                   = models.FloatField()
    yy                   = models.FloatField()

    # Relación con el lote de importación, ahora nullable
    carga = models.ForeignKey(
        RegistroCarga,
        on_delete=models.CASCADE,
        related_name='incidencias',
        null=True,
        blank=True,
        help_text="Lote de importación al que pertenece esta incidencia"
    )

    class Meta:
        db_table = 'incidencias_violenciafamiliar'
        managed = True

    def __str__(self):
        return f"Denuncia {self.num_denuncia} - {self.nombre} {self.apellido_paterno}"
