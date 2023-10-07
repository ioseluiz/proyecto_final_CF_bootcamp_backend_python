from django.db import models


class Terminal(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Route(models.Model):
    distance = models.DecimalField(max_digits=10,decimal_places=2)
    duration = models.DecimalField(max_digits=10, decimal_places=1)
    origin = models.ForeignKey(Terminal,on_delete=models.CASCADE, related_name='terminal_origin')
    destination = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name='terminal_destination')

    def __str__(self) -> str:
        return f"{self.origin.name} - {self.destination.name}"

