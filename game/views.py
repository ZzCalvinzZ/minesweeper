from django.shortcuts import render
from django.core.urlresolvers import reverse
from game.forms import GameForm
from game.models import Game, User, Coordinate
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json
from game.functions import reveal, create_revealed_matrix, set_flag_func, check_multiple_func, update_coordinates, reveal_mines, mine_exists, create_high_scores
from itertools import chain
from django.utils.datastructures import SortedDict

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
      try:
        user = User.objects.get(name=post['name'])
      except User.DoesNotExist:
        return HttpResponse('database error', status=404)  

      #create the game including minefield then save it to database
      if post['difficulty'] == 'beginner':
        game = Game(width=9,height=9,number_of_mines=10,difficulty='beginner',user=user)
      elif post['difficulty'] == 'intermediate':
        game = Game(width=16,height=16,number_of_mines=40,difficulty='intermediate',user=user)
      elif post['difficulty'] == 'expert':
        game = Game(width=30,height=16,number_of_mines=99,difficulty='expert',user=user)
      game.create_minefield()
      game.fields_left = game.width * game.height
      game.save()

      #redirect to the game page
      args = {'name': user.name, 'game_id': str(game.id)}
      return HttpResponseRedirect(reverse('game_start', kwargs=args))
  else:
    form = GameForm()

  top_beginner_users = User.objects.filter(game__difficulty='beginner', game__won=True).order_by('game__won')
  beginner_dict = create_high_scores(top_beginner_users)

  top_inter_users = User.objects.filter(game__difficulty='intermediate', game__won=True)
  inter_dict = create_high_scores(top_inter_users)

  top_expert_users = User.objects.filter(game__difficulty='expert', game__won=True)
  expert_dict = create_high_scores(top_expert_users)

  return render(request, 'index.html', {
      'form': form, 
      'beginner_dict': beginner_dict, 
      'inter_dict': inter_dict,
      'expert_dict': expert_dict
      })

def game_start(request, name, game_id):

  #get the current game from the passed in game id
  try:
    game = Game.objects.get(id=game_id)
  except Game.DoesNotExist:
    return HttpResponse('database error', status=404)  

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
    'fields_left' : game.fields_left,
    'game_number': game_number,
    'temp_coords': [],
    'won' : False,
    'lost': False
  }

  response = request.session['game_data']

  return render (request, 'game.html', response)

def game_check(request, name, game_id):
  try:
    game = Game.objects.get(id=game_id)
  except Game.DoesNotExist:
    return HttpResponse('database error', status=404)  

  #get the current game data from session
  game_data = request.session['game_data']

  # get info from the get requests (if applicable)
  if request.GET.get('x') != None: x = int(request.GET.get('x')) 
  if request.GET.get('y') != None: y = int(request.GET.get('y')) 
  set_flag = bool(request.GET.get('setFlag'))
  check_multiple = bool(request.GET.get('checkMultiple'))
  reload_data = bool(request.GET.get('reloadData'))

  #populate the session coordinates with the coordinates from the database
  if reload_data:
    coordinates = Coordinate.objects.filter(game=game)
    if coordinates.count > 0:
      for coord in coordinates:
        game_data['revealed_matrix'][coord.x][coord.y]['attr'] = coord.attr
    game_data['fields_left'] = game.fields_left
  else:
    # if the user wants to set a flag, only do this
    if set_flag:
      set_flag_func(x, y, game_data)
    # if the player is checking multiple fields at once via   
    elif check_multiple:
      if check_multiple_func(x, y, game_data):
        game_data['lost'] = True
        game.lost = True
        print "hello"
    # check ONE field (the one the player has clicked) 
    else:
      if mine_exists(x, y, game_data): 
        reveal_mines(game_data)
        game_data['revealed_matrix'][x][y]['attr'] = 'mine'
        game_data['lost'] = True
        game.lost = True
      else:
        reveal(x, y, game_data) 

    # Check for game win  
    if game_data['fields_left'] == game_data['mines']:
      game_data['won'] = True
      game.won = True

  #save the field left on database in case the game gets reloaded  
  game.fields_left = game_data['fields_left']
  game.save()

  # update the coordinates in the database under one save operation
  update_coordinates(game_data)
  game_data['temp_coords'] = []

  #save the data back onto the session
  request.session['game_data'] = game_data


  return HttpResponse(json.dumps(game_data), mimetype='application/json')