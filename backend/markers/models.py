from django.db import models

# Create your models here.


class Picture(models.Model):
    image = models.ImageField(
        verbose_name = "Изображение", 
        blank = False
    )
    
    name = models.CharField(
        max_length = 255,
        verbose_name = "Название", 
        blank = False
    )

    description = models.TextField(
        max_length=511,
        verbose_name = "Описание",
        blank = True, 
        null = True
    )

    def to_dict(self):
        return {
            'id': self.id,
            'picture': self.image.url,
            'name': self.name,
            'description': self.description,
            'markers': [marker.to_dict() for marker in self.marker_set.all()]
        }

    def __str__(self):
        return "<Picture: {} - {}>".format(self.id, self.name)


class Marker(models.Model):
    picture = models.ForeignKey(
        to = Picture, 
        verbose_name = 'Отображается на изображении',
        on_delete = models.CASCADE
    )
    
    to = models.ForeignKey(
        to = Picture, 
        verbose_name = 'Направляет на',
        on_delete = models.CASCADE, 
        related_name = "from_marker",
        unique = False
    )

    pos_x = models.FloatField(verbose_name = "Координата по X")
    pos_y = models.FloatField(verbose_name = "Координата по Y")

    text = models.CharField(
        max_length = 127, 
        verbose_name = "Текст маркера"
    )

    def to_dict(self):
        return {
            "to": self.to.id,
            "position": [self.pos_x, self.pos_y],
            "text": self.text
        }

    def __str__(self):
        return "<Marker for Picture {} (ID: {}); To: {} (ID: {})>".format(
            self.picture.name, 
            self.picture.id,
            self.to.name,
            self.to.id
        )