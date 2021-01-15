from django.db import models

class Nodes(models.Model):
    node_type = models.CharField(max_length=30)
    node_key = models.UUIDField(max_length=30)
    node_id = models.IntegerField(max_length=30)
    node_port = models.IntegerField(max_length=5)