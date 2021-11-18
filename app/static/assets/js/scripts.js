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

// Get the modal
var modal = document.getElementById("deletePostModal");

// Get the button that opens the modal
var btn = document.getElementById("deletePostBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("deletePost-close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}