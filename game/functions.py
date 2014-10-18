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
  coords = get_coords(x,y)
  recurse_more = True

  #first check if a mine exists anywhere adjacent
  for pair in coords:
    if not out_of_bounds(pair[0], pair[1], game_data):
      if mine_exists(pair[0], pair[1], game_data):
        game_data['revealed_matrix'][x][y]['count'] += 1
        recurse_more = False

  #recurse further out only if there is no adjacent mine
  if recurse_more:      
    for pair in coords:
      if not out_of_bounds(pair[0], pair[1], game_data):
        reveal_outer_cell(pair[0], pair[1], game_data)

  if game_data['revealed_matrix'][x][y]['attr'] == 'closed':
    game_data['fields_left'] -= 1
  game_data['revealed_matrix'][x][y]['attr'] = 'empty' + str(game_data['revealed_matrix'][x][y]['count'])
  
#reveals an outer_block then calls to reveal more outer blocks
def reveal_outer_cell(x, y, game_data):
  if game_data['revealed_matrix'][x][y]['attr'] == 'closed':
    if mine_exists(x, y, game_data):
      return
    else:
      game_data['revealed_matrix'][x][y]['attr'] = 'empty'
      game_data['fields_left'] -= 1
      reveal(x, y, game_data)

def out_of_bounds(x, y, game_data):
  if (x < 0 or x >= game_data['height']) or (y < 0 or y >= game_data['width']):
    return True
  else:
    return False

def get_coords(x, y):
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