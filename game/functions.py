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
def mine_exists(x, y, game_data):
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
      if mine_exists(pair[0], pair[1], game_data):
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
  coord_info = {
    'x':x,
    'y':y,
    'attr':game_data['revealed_matrix'][x][y]['attr']
  }
  game_data['temp_coords'].append(coord_info)
  
#reveals an outer_block then calls to reveal more outer blocks
def _reveal_outer_cell(x, y, game_data):
  if game_data['revealed_matrix'][x][y]['attr'] == 'closed':
    if mine_exists(x, y, game_data):
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
    game_data['temp_coords'].append({'x':x,'y':y,'attr':game_data['revealed_matrix'][x][y]['attr']})
  elif game_data['revealed_matrix'][x][y]['attr'] == 'flag':
    game_data['revealed_matrix'][x][y]['attr'] = 'closed'
    game_data['temp_coords'].append({'x':x,'y':y,'attr':game_data['revealed_matrix'][x][y]['attr']})

def reveal_mines(game_data):
  for x in range(0, game_data['height']):
    for y in range(0, game_data['width']):
      if mine_exists(x, y, game_data):
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
          if mine_exists(pair[0],pair[1], game_data):
            reveal_mines(game_data)
            game_data['revealed_matrix'][pair[0]][pair[1]]['attr'] = 'mine'
            return True
          else:  
            reveal(pair[0], pair[1], game_data) 

def update_coordinates(game_data):
  try:
    game = Game.objects.get(id=game_data['game_id'])
  except Game.DoesNotExist:
    return HttpResponse('database error', status=404)

  bulk_data = []  
  for coord in game_data['temp_coords']:
    bulk_data.append(Coordinate(x=coord['x'],y=coord['y'],attr=coord['attr'],game=game))
  Coordinate.objects.bulk_create(bulk_data)