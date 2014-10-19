$(document).ready(function() {

  var lost = false
  var win = false

  $('#mine-field').bind('contextmenu', function(e) {
      return false;
  }); 

  // check the field when it is clicked
  $('#mine-field tbody tr td').click(function (e){
    var target = e.target;
    //note x is row because the minefield is mapped as an array
    var x = target.parentNode.rowIndex;
    var y = target.cellIndex;

    if ($(target).hasClass('closed')) {
      check(x, y);
    }
  });

  // when a field is right clicked set a flag
  $('#mine-field tbody tr td').mousedown(function(e){ 
    if( e.button == 2 ) { 
      var target = e.target;

      //note x is row because the minefield is mapped as an array
      var x = target.parentNode.rowIndex;
      var y = target.cellIndex;

      if ($(target).is('.empty1, .empty2, .empty3, .empty4, .empty5, .empty6, .empty7')){
        checkMultiple(x, y);
      }
      else{
        setFlag(x, y);
      }
      return false; 
    } 
    return true; 
  }); 

  function check(x, y){

    $.ajax({
      url: window.location.pathname+ '/check',
      data: {
        x: x,
        y: y
      },
      success: function(response){
        if (lost == false && win == false){
          if (response.lost == true){
            lost = true
            gameLost();
          } 

          if (response.won == true){
            win = true
            gameWon();
          } 

          remap(response);        
        }
      },
      error: function(response){
        alert('something went wrong, please try again');
      }
    });
  }
  
  function setFlag(x, y){
        $.ajax({
      url: window.location.pathname+ '/check',
      data: {
        x: x,
        y: y,
        setFlag: true
      },
      success: function(response){
        remap(response);        
      },
      error: function(response){
        alert('something went wrong, please try again');
      }
    });
  }

  function checkMultiple(x, y){
        $.ajax({
      url: window.location.pathname+ '/check',
      data: {
        x: x,
        y: y,
        checkMultiple: true
      },
      success: function(response){
        if (lost == false && win == false){
          if (response.lost == true){
            lost = true
            gameLost();
          } 

          if (response.won == true){
            win = true
            gameWon();
          } 

          remap(response);        
        }        
      },
      error: function(response){
        alert('something went wrong, please try again');
      }
    });
  }

  function remap(response){
    for (var i=0; i<response.height; i++){
      for (var j=0; j<response.width; j++){
        var $cell = $('#mine-field tbody tr:eq('+i+') td:eq('+j+')');
        var responseCell = response.revealed_matrix[i][j];
        if ($cell.attr('class') !== responseCell.attr) {
          setNewAttr($cell, responseCell);
        }
      }
    }
  }

  function setNewAttr($cell, responseCell){
    $cell.removeClass().addClass(responseCell.attr)

    //if cell is empty show how many mines are nearby
    if ($cell.attr('class').slice(0,5) === 'empty'){
      var noOfMines = $cell.attr('class').slice(-1);
      if (noOfMines !== '0'){
        $cell.text(noOfMines);
      }
    }
    else if ($cell.attr('class') === 'mine' || $cell.attr('class') === 'rev-mine'){
      $cell.text('@')
    }
    else if ($cell.attr('class') === 'flag'){
      $cell.text('|>')
    }
    else if ($cell.attr('class') === 'closed'){
      $cell.text('')
    }
  }

  function gameLost(){
    $('#complete').html("<p>You Lose! Sorry about that,<a href='/'>click here</a> to try again</p>")
  }

  function gameWon(){
    $('#complete').html("<p>You Win! Congratulations,<a href='/'>click here</a> to try again</p>")
  }
});
