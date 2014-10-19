from django.shortcuts import render
from django.core.urlresolvers import reverse
from game.forms import GameForm
from game.models import Game, User
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json
from game.functions import reveal, mine_exists, create_revealed_matrix, set_flag_func, reveal_mines, check_multiple_func, player_loses, check_for_win

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

  if game.won or game.lost:
    return HttpResponseRedirect(reverse('index'))

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
    'fields_left' : game.width * game.height,
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
  set_flag = bool(request.GET.get('setFlag'))
  check_multiple = bool(request.GET.get('checkMultiple'))

  # if the user wants to set a flag, only do this
  if set_flag:
    set_flag_func(x, y, game_data)
  # if the player is checking multiple fields at once via   
  elif check_multiple:
    check_multiple_func(x, y, game_data)
  # check ONE field (the one the player has clicked) 
  else:
    if not player_loses(x, y, game_data):
      reveal(x, y, game_data) 

  print game_data['fields_left'] == game_data['mines']
  # Check for game win  
  check_for_win(x, y, game_data)

  #save the data back onto the session
  request.session['game_data'] = game_data

  return HttpResponse(json.dumps(game_data), mimetype='application/json')