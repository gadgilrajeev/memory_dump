//// Open the popup when the form is submitted
//document.getElementById('popupBtn').addEventListener('click', function(event) {
////  event.preventDefault(); // Prevent form submission
//
//  var startAddress = document.getElementById('start_address').value;
//  var endAddress = document.getElementById('end_address').value;
//  var interval = document.getElementById('interval').value;
//  var iterations = document.getElementById('iterations').value;
//
//  var popup = document.getElementById('popup');
//  var popupContent = popup.getElementsByClassName('popup-content')[0];
//  var popupMessage = document.createElement('p');
//
//  popupMessage.innerHTML = "Running C file with arguments:<br>Start Address: " + startAddress + "<br>End Address: " + endAddress + "<br>Interval: " + interval + "<br>Iterations: " + iterations;
////    // Remove previous message
////    while (popupContent.firstChild) {
////      popupContent.firstChild.remove();
////    }
//  // Append the message to the popup content
//  popupContent.appendChild(popupMessage);
//
//  popup.style.display = 'block';
//
//});
//
//// Close the popup when the close button is clicked
//document.getElementsByClassName('close')[0].addEventListener('click', function() {
//  document.getElementById('popup').style.display = 'none';
//});

document.getElementById('popupBtn').addEventListener('click', function(event) {
//  event.preventDefault(); // Prevent form submission

  var startAddress = document.getElementById('start_address').value;
  var endAddress = document.getElementById('end_address').value;
  var interval = document.getElementById('interval').value;
  var iterations = document.getElementById('iterations').value;

  var popup = document.getElementById('popup');
  var popupContent = popup.getElementsByClassName('popup-content')[0];
  var popupMessage = document.createElement('p');

  if (startAddress && endAddress && interval && iterations) {
    popupMessage.innerHTML = "Running file with arguments:<br>Start Address: " + startAddress + "<br>End Address: " + endAddress + "<br>Interval: " + interval + "<br>Iterations: " + iterations;

    // Append the new message to the popup content
    popupContent.appendChild(popupMessage);

    popup.style.display = 'block';
  }
});

document.getElementsByClassName('close')[0].addEventListener('click', function() {
  document.getElementById('popup').style.display = 'none';
});
