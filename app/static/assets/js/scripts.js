/* Open */
function openNav() {
    document.getElementById("search-container").style.height = "100%";
  }
  
  /* Close */
  function closeNav() {
    document.getElementById("search-container").style.height = "0%";
  }

  $('.search-button').click(function(){
    $(this).parent().toggleClass('open');
  });

  // category_select = document.getElementById('category');

  // category_select.onchange = function() {
  //   category = category_select.value;
  //   alert(category)
  // }