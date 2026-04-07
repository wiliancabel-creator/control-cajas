from django.db import models, transaction
from django.core.exceptions import ValidationError


class TipoCaja(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    prefijo = models.CharField(max_length=20, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Tipo de caja'
        verbose_name_plural = 'Tipos de caja'

    def __str__(self):
        return f"{self.nombre} ({self.prefijo})"


class Caja(models.Model):
    tipo_caja = models.ForeignKey(TipoCaja, on_delete=models.PROTECT, related_name='cajas')
    codigo = models.CharField(max_length=50, unique=True, blank=True)
    correlativo = models.PositiveIntegerField(default=0, editable=False)

    tecnico = models.CharField(max_length=100, blank=True, null=True)
    ubicacion = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'

    def __str__(self):
        return self.codigo

    def clean(self):
        if not self.tipo_caja:
            raise ValidationError("Debes seleccionar un tipo de caja.")

    def generar_codigo(self):
        if not self.tipo_caja:
            raise ValidationError("No se puede generar el código sin tipo de caja.")

        with transaction.atomic():
            ultima = (
                Caja.objects.select_for_update()
                .filter(tipo_caja=self.tipo_caja)
                .order_by('-correlativo')
                .first()
            )

            siguiente = 1 if not ultima else ultima.correlativo + 1
            self.correlativo = siguiente
            self.codigo = f"{self.tipo_caja.prefijo}-{siguiente:03d}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.generar_codigo()
        super().save(*args, **kwargs)