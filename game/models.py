from django.db import models

# Create your models here.
class Game(models.Model):
  time = models.IntegerField(default=0)
  number_of_mines = models.IntegerField(default=0)
  difficulty = models.CharField(max_length=200)
  height = models.IntegerField(default=0)
  width = models.IntegerField(default=0)
  mine_field = models.CharField(max_length=100000)


class User(models.Model):
  name = models.CharField(max_length=200)
  game = models.ForeignKey(Game)
