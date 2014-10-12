from django.db import models

# Create your models here.
class Game(models.Model):
  time = models.IntegerField(default=0)
  number_of_mines = models.IntegerField(default=0)
  difficulty = models.CharField(max_length=200)
  height = models.IntegerField(default=0)
  width = models.IntegerField(default=0)
  mine_field = models.CharField(max_length=100000)

  def __init__(self, x, y, number_of_mines):
    self.number_of_mines = number_of_mines
    self.width = x
    self.height = y
    self.mine_field = create_minefield()

  def _minefield_array_to_char(self, mine_field):
    mine_field_string = ""
    for x in range(0, self.height):
      for y in range(0, self.width):
        mine_field_string += mine_field[x][y]
    return mine_field_string

#  def get_minefield_array(self):


  def _create_minefield(self):
    mine_field = []
    for x in range(0, self.height):
      for y in range(0, self.width):
        mine_field[x][y] = 0

    for n in range(0,self.number_of_mines):

      while True:
        x = randint(0, self.height)
        y = randint(0, self.width)
        if mine_field[x][y] != 1:
          mine_field[x][y] = 1
          break
    return _minefield_array_to_char(mine_field)


class User(models.Model):
  name = models.CharField(max_length=200)
  game = models.ForeignKey(Game)
