 $(document).ready(function() {

  var lost = false
  var win = false

  $('#mine-field tbody tr td').click(function (e){
    var target = e.target;
    //note x is row because the minefield is mapped as an array
    var x = target.parentNode.rowIndex;
    var y = target.cellIndex;

    if ($(target).hasClass('closed')) {
      check(x, y);
    }
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
        alert(response.test);
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
    if ($cell.attr('class') === 'mine'){
      $cell.text('@')
    }
  }

  function gameLost(){
    $('#complete').html("<p>You Lose! Sorry about that,<a href='/'>click here</a> to try again</p>")
  }

  function gameWon(){
    $('#complete').html("<p>You Win! Congratulations,<a href='/'>click here</a> to try again</p>")
  }
});
