var sentinel = document.querySelector('#sentinel');
// Function to request new items and render to the dom
function loadItems() {
    sentinel.innerHTML = "";
    sentinel.style.display = "none";

    // Use fetch to request data and pass the counter value in the QS
    fetch(`/jobs?jid=${ids}`).then((response) => {

        // Convert the response data to JSON
        response.json().then((data) => {
            $('#main').append(data[0]);
        })
})
}

var intersectionObserver = new IntersectionObserver(entries => {

    // Uncomment below to see the entry.intersectionRatio when
    // the sentinel comes into view
  
    // entries.forEach(entry => {
    //   console.log(entry.intersectionRatio);
    // })
  
    // If intersectionRatio is 0, the sentinel is out of view
    // and we don't need to do anything. Exit the function
    if (entries[0].intersectionRatio <= 0) {
      return;
    }
  
    // Call the loadItems function
    loadItems();
  
});

if ($("#id").length > 0){
  var ids = $("#id").text();
} else {
  var ids = "none"
}

intersectionObserver.observe(sentinel);