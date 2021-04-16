from django.db import models

class contabilizador_visitas(models.Model):
    id_visita_web = models.AutoField(primary_key=True)
    fch_visita_web = models.DateTimeField(auto_now_add=True)
    ip_visita_web = models.CharField(max_length=50, blank=True,null=True)
