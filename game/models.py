from django.db import models
import random
from django.db.models.signals import post_init

class User(models.Model):
  name = models.CharField(max_length=200)

  def __unicode__(self):
        return self.name

class Game(models.Model):
  time = models.IntegerField(default=0)
  number_of_mines = models.IntegerField(default=0)
  difficulty = models.CharField(max_length=200)
  height = models.IntegerField(default=0)
  width = models.IntegerField(default=0)
  mine_field = models.CharField(max_length=100000, default="")
  user = models.ForeignKey(User)
  won = models.BooleanField(default=False)
  lost = models.BooleanField(default=False)
  fields_left = models.IntegerField(default=0)

  # initialize a new game object setting the minefield
  # def __init__(self, x, y, number_of_mines, difficulty):
  #   self.number_of_mines = number_of_mines
  #   self.width = x
  #   self.height = y
  #   self.mine_field = self._create_minefield()
  #   self.difficulty = difficulty

  # convert the Array that maps the minefield to a String
  def _minefield_array_to_char(self, mine_field):
    mine_field_string = ""
    for row in mine_field:
      for field in row:
        mine_field_string += field
    return mine_field_string

  #  convert the stored string representation of the minefield an array
  def get_minefield_array(self):
    char = 0
    mine_field = []
    for x in range(0, self.height):
      row = []
      for y in range(0, self.width):
        row.append(self.mine_field[char])
        char += 1
      mine_field.append(row)  
    return tuple(mine_field)

  # Creates the minefield and returns the string representation
  def create_minefield(self):
    mine_field = []
    for x in range(0, self.height):
      row = []
      for y in range(0, self.width):
        row.append('E')
      mine_field.append(row)

    for n in range(0,self.number_of_mines):

      while True:
        x = random.randint(0, self.height -1)
        y = random.randint(0, self.width -1)
        if mine_field[x][y] != 'M':
          mine_field[x][y] = 'M'
          break

    self.mine_field = self._minefield_array_to_char(mine_field)

  def __unicode__(self):
    return self.difficulty

class Coordinate(models.Model):
  x = models.IntegerField(default=0)
  y = models.IntegerField(default=0)
  attr = models.CharField(max_length=10, default="closed")
  game = models.ForeignKey(Game)