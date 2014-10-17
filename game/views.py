from django.shortcuts import render
from game.forms import GameForm
from game.models import Game, User
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json

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
    'game_number': game_number
  }
  return render (request, 'game.html', request.session['game_data'])

def game_check(request, name, game_id):
  #get the current game data from session
  game_data = request.session['game_data']
  game = Game.objects.get(id=game_id)

  x = int(request.GET.get('x'))
  y = int(request.GET.get('y'))

  if check_for_mine(x, y, game_data):
    lost = true
  else:
    reveal(x, y, game_data)  


  if request.session['game_data']:
    return HttpResponse(json.dumps({'test': 'it works'}), mimetype='application/json')