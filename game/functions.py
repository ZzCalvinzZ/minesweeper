from game.models import Game, User, Coordinate
from django.http import HttpResponse

# Creates the matrix that keeps track of whats been revealed
def create_revealed_matrix(height, width):
  revealed_matrix = []
  for x in range(0, height):
    row = []
    for y in range(0, width):
      row.append({'attr':'closed', 'count':0})
    revealed_matrix.append(row)
  return revealed_matrix  

#determines whether or not a mine exists in the coordinate
def _mine_exists(x, y, game_data):
  mine_field = game_data['mine_field']
  if mine_field[x][y] == 'M':
    return True
  else:
    return False

#reveals the blocks around the current block
def reveal(x, y, game_data):
  coords = _get_coords(x,y)
  recurse_more = True

  #first check if a mine exists anywhere adjacent
  for pair in coords:
    if not _out_of_bounds(pair[0], pair[1], game_data):
      if _mine_exists(pair[0], pair[1], game_data):
        game_data['revealed_matrix'][x][y]['count'] += 1
        recurse_more = False

  #recurse further out only if there is no adjacent mine
  if recurse_more:      
    for pair in coords:
      if not _out_of_bounds(pair[0], pair[1], game_data):
        _reveal_outer_cell(pair[0], pair[1], game_data)

  if game_data['revealed_matrix'][x][y]['attr'] == 'closed':
    game_data['fields_left'] -= 1
  game_data['revealed_matrix'][x][y]['attr'] = 'empty' + str(game_data['revealed_matrix'][x][y]['count'])
  _update_coordinate(x, y, game_data['revealed_matrix'][x][y]['attr'], game_data['game_id'])
  
#reveals an outer_block then calls to reveal more outer blocks
def _reveal_outer_cell(x, y, game_data):
  if game_data['revealed_matrix'][x][y]['attr'] == 'closed':
    if _mine_exists(x, y, game_data):
      return
    else:
      game_data['revealed_matrix'][x][y]['attr'] = 'empty'
      game_data['fields_left'] -= 1
      reveal(x, y, game_data)

def _out_of_bounds(x, y, game_data):
  if (x < 0 or x >= game_data['height']) or (y < 0 or y >= game_data['width']):
    return True
  else:
    return False

def _get_coords(x, y):
  coords = [
    [x-1, y],
    [x-1, y-1],
    [x, y-1],
    [x+1, y-1],
    [x+1, y],
    [x+1, y+1],
    [x, y+1],
    [x-1, y+1]
  ]
  return coords

# set the flag, if its already set then change it to closed
def set_flag_func(x, y, game_data):
  if game_data['revealed_matrix'][x][y]['attr'] == 'closed':
    game_data['revealed_matrix'][x][y]['attr'] = 'flag'
    _update_coordinate(x, y, game_data['revealed_matrix'][x][y]['attr'], game_data['game_id'])
  elif game_data['revealed_matrix'][x][y]['attr'] == 'flag':
    game_data['revealed_matrix'][x][y]['attr'] = 'closed'
    _update_coordinate(x, y, game_data['revealed_matrix'][x][y]['attr'], game_data['game_id'])

def _reveal_mines(game_data):
  for x in range(0, game_data['height']):
    for y in range(0, game_data['width']):
      if _mine_exists(x, y, game_data):
        game_data['revealed_matrix'][x][y]['attr'] = 'rev-mine'

def check_multiple_func(x, y, game_data):
  coords = _get_coords(x,y)
  flag_exists = False
  #first check if a flag exists anywhere adjacent
  for pair in coords:
    if not _out_of_bounds(pair[0], pair[1], game_data):
      if game_data['revealed_matrix'][pair[0]][pair[1]]['attr'] == 'flag':
        flag_exists = True

  if flag_exists:
    for pair in coords:
      if not _out_of_bounds(pair[0], pair[1], game_data): 
        if game_data['revealed_matrix'][pair[0]][pair[1]]['attr'] == 'closed':
          if not player_loses(pair[0], pair[1], game_data):
            reveal(pair[0], pair[1], game_data) 


def player_loses(x, y, game_data):
  try:
    game = Game.objects.get(id=game_data['game_id'])
  except Game.DoesNotExist:
    return HttpResponse('database error', status=404) 
    
  if _mine_exists(x, y, game_data): 
    _reveal_mines(game_data)
    game_data['revealed_matrix'][x][y]['attr'] = 'mine'
    game_data['lost'] = True
    game.lost = True
    game.save()
    return True
  else:
    return False

def check_for_win(x, y, game_data):
  try:
    game = Game.objects.get(id=game_data['game_id'])
  except Game.DoesNotExist:
    return HttpResponse('database error', status=404) 

  if game_data['fields_left'] == game_data['mines']:
    game_data['won'] = True
    game.won = True
    game.save()

def _update_coordinate(x, y, attr, game_id):
  try:
    game = Game.objects.get(id=game_id)
  except Game.DoesNotExist:
    return HttpResponse('database error', status=404)

  coordinate = Coordinate(x=x, y=y, attr= attr, game=game)
  coordinate.save()