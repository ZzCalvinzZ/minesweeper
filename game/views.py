from django.shortcuts import render
from game.forms import GameForm
from game.models import Game, User
from django.http import HttpResponseRedirect

def index(request):
  if request.method == 'POST':
    post = (request.POST)
    form = GameForm(post)
    if form.is_valid():
      #create the user if they don't exist already
      user = User.objects.filter(name=post['name'])[:1]
      if not user:
        new_user = User(name=post['name'])
        new_user.save()
      user = User.objects.get(name=post['name'])

      #create the game including minefield then save it to database
      if post['difficulty'] == 'beginner':
        game = Game(width=9,height=9,number_of_mines=10,difficulty='beginner',user=user)
      elif post['difficulty'] == 'intermediate':
        game = Game(width=16,height=16,number_of_mines=40,difficulty='intermediate',user=user)
      elif post['difficulty'] == 'expert':
        game = Game(width=30,height=16,number_of_mines=99,difficulty='expert',user=user)
      game.create_minefield()
      game.save()

      #redirect to the game page
      url = '/game/'+ user.name + '/' + str(game.id)
      return HttpResponseRedirect(url)
  else:
    form = GameForm()

  return render(request, 'index.html', {'form': form})

def game_start(request, name, game_id):


  return render (request, 'game.html',{'name': name, 'game_id': game_id})