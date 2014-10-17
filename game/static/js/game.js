 $(document).ready(function() {

  $('.mine-field tbody tr td').click(function (e){
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
        alert(response.test)
      },
      error: function(response){
        alert(response.test)
      }
    });
  }
  
});