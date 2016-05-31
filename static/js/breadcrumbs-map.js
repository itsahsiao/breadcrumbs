"use strict";

// Define global variable so URL with user id for JSON can be passed into AJAX get request
var user_visits_json = "/users/" + $("#user-info").data("userid") + "/visits.json";

// Initialize map
function initMap() {
  
    // Specify where the map is centered
    // Re: coordinates - North is positive / South is negative / West is negative / East is positive
    // TODO: Center the map based on user's city (get coordinates for city)
    // Currently map center is hard coded with the coordinates for Sunnyvale
    var myLatLng = {lat: 37.3688, lng: -122.0363};

    // Create a map object and specify the DOM element for display
    var map = new google.maps.Map(document.getElementById('map'), {
        center: myLatLng,
        zoom: 13,
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        },
        streetViewControl: true,
        streetViewControlOptions: {
            position: google.maps.ControlPosition.LEFT_CENTER
        },
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.LEFT_CENTER
        },
    });

    // Resource used for multiple info windows:
    // http://you.arenot.me/2010/06/29/google-maps-api-v3-0-multiple-markers-multiple-infowindows/

    // Create a global variable for the info window within this function
    // This way, it changes the content each time when a marker is clicked
    var infoWindow = new google.maps.InfoWindow({
        maxWidth: 200
    });

    var iconImage = '/static/img/restaurant-marker.png';

    // Make AJAX call to server to get JSON that has info re: user's restaurant visits
    // For every restaurant that the user has visited, place markers on map and display
    // an info window when a marker is clicked
    $.get(user_visits_json, function (visits) {

        for (var key in visits) {
            var visit = visits[key];

            // Content of info window 
            // Display information about the restaurant
            var contentString = '<div id="content">' +
                '<h3>'+ visit.restaurant + '</h3>' +
                'Address: ' + visit.address + '<br>' +
                'Phone: ' + visit.phone +
                '</div>';

            // Specify marker coordinates with restaurant's coordinates
            var markerLatLng = {lat: visit.latitude, lng: visit.longitude};

            // Create a marker object
            var marker = new google.maps.Marker({
                position: markerLatLng,
                map: map,
                title: 'Restaurant: ' + visit.restaurant,
                html: contentString,
                icon: iconImage
            });

            // Add an event handler that sets content of info window to "this" 
            // marker being clicked and open the info window for "this" marker
            marker.addListener('click', function() {
                infoWindow.setContent(this.html);
                infoWindow.open(map, this);
            });

        }

    });
  
}