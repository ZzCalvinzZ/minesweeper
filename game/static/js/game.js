 $(document).ready(function() {

  $('#mine-field tbody tr td').click(function (e){
    var target = e.target;
    var y = target.parentNode.rowIndex;
    var x = target.cellIndex;

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
        console.log(response)
        if (response.lost == true){
          // gameLost();
        } 

        if (response.won == true){
          // gameWon();
        }

        remap(response);        

      },
      error: function(response){
        alert(response.test);
      }
    });
  }
  
  function remap(response){
    for (var i=0; i<response.height; i++){
      for (var j=0; j<response.width; j++){
        var $cell = $('#mine-field tbody tr:eq('+j+') td:eq('+i+')');
        var responseCell = response.revealed_matrix[i][j];
        if ($cell.attr('class') !== responseCell.attr) {
          $cell.removeClass().addClass(responseCell.attr)
        }
      }
    }
  }
});