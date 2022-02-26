// Inserting keyword


// document
//   .getElementById("keyword_input")
//   .addEventListener("click", function (event) {
//     event.preventDefault();
//     keyword_value = document.getElementById("keyword").value;
//     var xhr = new XMLHttpRequest();
//     xhr.open("GET", `http://localhost:8000/search/${keyword_value}`, true);
//     xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
//     xhr.onreadystatechange = function () {
//       if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
//         // let response = JSON.parse(xhr.responseText);
//         console.log('hello')
//       }
//     };
//     xhr.send();
//   });






  // Modal Javascript
  // Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}



