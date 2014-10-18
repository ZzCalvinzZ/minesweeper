from django.shortcuts import render
from django.core.urlresolvers import reverse
from game.forms import GameForm
from game.models import Game, User
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json
from game.functions import reveal, mine_exists, create_revealed_matrix

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
      args = {'name': user.name, 'game_id': str(game.id)}
      return HttpResponseRedirect(reverse('game_start', kwargs=args))
  else:
    form = GameForm()

  return render(request, 'index.html', {'form': form})

def game_start(request, name, game_id):
  #get the current game from the passed in game id
  game = Game.objects.get(id=game_id)
  game_number = Game.objects.filter(user__name=name).count()

  #save game info as session data for easy retrieval
  request.session['game_data'] = {
    'name': name,
    'game_id' : game_id,
    'mines': game.number_of_mines,
    'difficulty': game.difficulty,
    'height': game.height,
    'width': game.width,
    'mine_field': game.get_minefield_array(),
    'revealed_matrix': create_revealed_matrix(game.height, game.width),
    'game_number': game_number,
    'won' : False,
    'lost': False
  }

  request.session['tested_coords'] = []
  return render (request, 'game.html', request.session['game_data'])

def game_check(request, name, game_id):
  #get the current game data from session
  game_data = request.session['game_data']
  game = Game.objects.get(id=game_id)


  x = int(request.GET.get('x'))
  y = int(request.GET.get('y'))

  if mine_exists(x, y, game_data):
    game_data['revealed_matrix'][x][y]['attr'] = 'mine'
    game_data['lost'] = True
    print"bopabooyayayayayayatrallalalalalalalal"
  else:
    game_data['revealed_matrix'][x][y]['attr'] = 'empty0'
    reveal(x, y, game_data)  

  return HttpResponse(json.dumps(game_data), mimetype='application/json')