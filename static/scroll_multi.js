// Get references to the dom elements
var scroller = document.querySelector("#scroller");
var template = document.querySelector('#post_template');
var loaded = document.querySelector("#loaded");
var sentinel = document.querySelector('#sentinel');
var format = document.querySelector('.format');

// Set a counter to count the items loaded
var counter = 0;

// Function to request new items and render to the dom
function loadItems() {
  if (type == "all") {

    // Use fetch to request data and pass the counter value in the QS
    fetch(`/load?c=${counter}&s=${search}&company=${company}&l=${locationn}`).then((response) => {

      // Convert the response data to JSON
      response.json().then((data) => {

        // If empty JSON, exit the function
        if (!data.length) {

          // Replace the spinner with "No more posts"
          sentinel.innerHTML = "No more posts";
          return;
        }

        // Iterate over the items in the response
        for (var i = 0; i < data.length; i++) {

          // Clone the HTML template
          let template_clone = template.content.cloneNode(true);
          $('#mainContent').append(data[i]);

          // Query & update the template content
          //template_clone.querySelector("#title").innerHTML = `${data[i][0]}: ${data[i][1]}`;
          //template_clone.querySelector("#content").innerHTML = data[i][2];

          // Append template to dom
          scroller.appendChild(template_clone);

          // Increment the counter
          counter += 1;
        }
      })
    })
  } if (type == "both") {
    // Use fetch to request data and pass the counter value in the QS
    fetch(`/load?company=${company}&l=${locationn}&c=${counter}`).then((response) => {

      // Convert the response data to JSON
      response.json().then((data) => {

        // If empty JSON, exit the function
        if (!data.length) {

          // Replace the spinner with "No more posts"
          sentinel.innerHTML = "No more posts";
          return;
        }

        // Iterate over the items in the response
        for (var i = 0; i < data.length; i++) {

          // Clone the HTML template
          let template_clone = template.content.cloneNode(true);
          $('#mainContent').append(data[i]);

          // Query & update the template content
          //template_clone.querySelector("#title").innerHTML = `${data[i][0]}: ${data[i][1]}`;
          //template_clone.querySelector("#content").innerHTML = data[i][2];

          // Append template to dom
          scroller.appendChild(template_clone);

          // Increment the counter
          counter += 1;
        }
      })
    })
    } if (type == "jobs-at"){
        console.log('herejs');
        fetch(`/load?company=${company}&c=${counter}`).then((response) => {

            // Convert the response data to JSON
            response.json().then((data) => {
      
              // If empty JSON, exit the function
              if (!data.length) {
      
                // Replace the spinner with "No more posts"
                sentinel.innerHTML = "No more posts";
                return;
              }
      
              // Iterate over the items in the response
              for (var i = 0; i < data.length; i++) {
      
                // Clone the HTML template
                let template_clone = template.content.cloneNode(true);
                $('#mainContent').append(data[i]);
                console.log(data[i]);
                console.log(data.length);
      
                // Query & update the template content
                //template_clone.querySelector("#title").innerHTML = `${data[i][0]}: ${data[i][1]}`;
                //template_clone.querySelector("#content").innerHTML = data[i][2];
      
                // Append template to dom
                scroller.appendChild(template_clone);
      
                // Increment the counter
                counter += 1;
                console.log(counter);
              }
            })
          })
    } if (type == "jobs-in"){
      fetch(`/load?l=${locationn}&c=${counter}`).then((response) => {

          // Convert the response data to JSON
          response.json().then((data) => {
    
            // If empty JSON, exit the function
            if (!data.length) {
    
              // Replace the spinner with "No more posts"
              sentinel.innerHTML = "No more posts";
              return;
            }
    
            // Iterate over the items in the response
            for (var i = 0; i < data.length; i++) {
    
              // Clone the HTML template
              let template_clone = template.content.cloneNode(true);
              $('#mainContent').append(data[i]);
              console.log(data[i]);
              console.log(data.length);
    
              // Query & update the template content
              //template_clone.querySelector("#title").innerHTML = `${data[i][0]}: ${data[i][1]}`;
              //template_clone.querySelector("#content").innerHTML = data[i][2];
    
              // Append template to dom
              scroller.appendChild(template_clone);
    
              // Increment the counter
              counter += 1;
              console.log(counter);
            }
          })
        })
    } if (type == "sand"){
      fetch(`/load?s=${search}&l=${locationn}&c=${counter}`).then((response) => {

        // Convert the response data to JSON
        response.json().then((data) => {
  
          // If empty JSON, exit the function
          if (!data.length) {
  
            // Replace the spinner with "No more posts"
            sentinel.innerHTML = "No more posts";
            return;
          }
  
          // Iterate over the items in the response
          for (var i = 0; i < data.length; i++) {
  
            // Clone the HTML template
            let template_clone = template.content.cloneNode(true);
            $('#mainContent').append(data[i]);
            console.log(data[i]);
            console.log(data.length);
  
            // Query & update the template content
            //template_clone.querySelector("#title").innerHTML = `${data[i][0]}: ${data[i][1]}`;
            //template_clone.querySelector("#content").innerHTML = data[i][2];
  
            // Append template to dom
            scroller.appendChild(template_clone);
  
            // Increment the counter
            counter += 1;
            console.log(counter);
          }
        })
      })
    }
}

// Create a new IntersectionObserver instance
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
  console.log('herejs1')
  loadItems();

});

// Instruct the IntersectionObserver to watch the sentinel
if ($("#reqType").length > 0){
  var type = $("#reqType").text();
  console.log(type)
} else {
  var search = "none"
}

if (type == "all") {
    var dataa = $("#searchTermDataa").text();
    var locationn = dataa.split(':')[1];
    var company = dataa.split(':')[0];
    var search = dataa.split(':')[2];
} if (type == "both") {
    var dataa = $("#searchTermDataa").text();
    var locationn = dataa.split(':')[1];
    var company = dataa.split(':')[0];
} if (type == "jobs-at") { 
    var dataa = $("#searchTermDataa").text();
    var company = dataa;
} if (type == "jobs-in") {
    var dataa = $("#searchTermDataa").text();
    var locationn = dataa;
} if (type == "sand") {
    var dataa = $("#searchTermDataa").text();
    var search = dataa[1];
    var locationn = dataa[0];
}

intersectionObserver.observe(sentinel);

