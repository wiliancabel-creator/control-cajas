from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Empresa(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nombre


class UsuarioEmpresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario_empresa')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='usuarios')

    class Meta:
        verbose_name = 'Usuario de empresa'
        verbose_name_plural = 'Usuarios de empresa'

    def __str__(self):
        return f"{self.user.username} - {self.empresa.nombre}"


class TipoCaja(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='tipos_caja')
    nombre = models.CharField(max_length=100)
    prefijo = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Tipo de caja'
        verbose_name_plural = 'Tipos de caja'
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'nombre'], name='uq_tipo_nombre_empresa'),
            models.UniqueConstraint(fields=['empresa', 'prefijo'], name='uq_tipo_prefijo_empresa'),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.prefijo})"


class SecuenciaCaja(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='secuencias_caja')
    tipo_caja = models.OneToOneField(TipoCaja, on_delete=models.CASCADE, related_name='secuencia')
    ultimo_numero = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Secuencia de caja'
        verbose_name_plural = 'Secuencias de caja'
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'tipo_caja'], name='uq_secuencia_empresa_tipo'),
        ]

    def __str__(self):
        return f"{self.empresa.nombre} - {self.tipo_caja.prefijo} - {self.ultimo_numero}"


class Caja(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='cajas')
    tipo_caja = models.ForeignKey(TipoCaja, on_delete=models.PROTECT, related_name='cajas')
    codigo = models.CharField(max_length=50, blank=True)
    correlativo = models.PositiveIntegerField(default=0, editable=False)

    tecnico = models.CharField(max_length=100, blank=True, null=True)
    ubicacion = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'codigo'], name='uq_codigo_empresa'),
        ]

    def __str__(self):
        return self.codigo or "Sin código"

    def clean(self):
        if not self.empresa:
            raise ValidationError("La empresa es obligatoria.")

        if not self.tipo_caja:
            raise ValidationError("Debes seleccionar un tipo de caja.")

        if self.tipo_caja.empresa_id != self.empresa_id:
            raise ValidationError("El tipo de caja no pertenece a la empresa seleccionada.")

    def generar_codigo(self):
        if not self.empresa or not self.tipo_caja:
            raise ValidationError("No se puede generar el código sin empresa y tipo de caja.")

        with transaction.atomic():
            secuencia, _ = SecuenciaCaja.objects.select_for_update().get_or_create(
                empresa=self.empresa,
                tipo_caja=self.tipo_caja,
                defaults={'ultimo_numero': 0}
            )

            siguiente = secuencia.ultimo_numero + 1
            self.correlativo = siguiente
            self.codigo = f"{self.tipo_caja.prefijo}-{siguiente:03d}"

            secuencia.ultimo_numero = siguiente
            secuencia.save()

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.codigo:
            self.generar_codigo()

        super().save(*args, **kwargs)