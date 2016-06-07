"use strict";

// URL (string) to pass into AJAX get request
var user_visits_json = "/users/" + $("#user-info").data("userid") + "/visits.json";

function initMap() {
  
    // Specify where the map is centered (currently set as Sunnyvale)t
    var myLatLng = {lat: 37.3688, lng: -122.0363};

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

    // Create a global info window which the content within changes each time a marker is clicked
    var infoWindow = new google.maps.InfoWindow({
        maxWidth: 250
    });

    var iconImage = '/static/img/restaurant-marker.png';

    // Get JSON for user's restaurant visits with the response passed into the function
    $.get(user_visits_json, function (visits) {

        // For every restaurant that the user has visited, specify restaurant details and place markers
        for (var key in visits) {
            var visit = visits[key];

            var restaurantDetails = '<div class="media">' +
                    '<a href="/restaurants/' + visit.rest_id + '">' +
                    '<div class="media-left">' +
                    '<img class="media-object" src="' + visit.image_url + '" alt="Image for' + visit.restaurant + '">' +
                    '</div>' +
                    '<div class="media-body">' +
                    '<h5 class="media-heading">' + visit.restaurant + '</h5>' +
                    '<p>' +
                    '<span class="glyphicon glyphicon-map-marker" aria-hidden="true"></span> ' + visit.address + '<br>' +
                    '<span class="glyphicon glyphicon-earphone" aria-hidden="true"></span> ' + visit.phone +
                    '</p>' +
                    '</div>' +
                    '</a>' +
                    '</div>';

            // Specify marker coordinates with the restaurant's coordinates
            var markerLatLng = {lat: visit.latitude, lng: visit.longitude};

            var marker = new google.maps.Marker({
                position: markerLatLng,
                map: map,
                title: 'Restaurant: ' + visit.restaurant,
                html: restaurantDetails,
                icon: iconImage
            });

            // When a marker is clicked, set content to restaurant details for "this" marker and open "this"
            marker.addListener('click', function() {
                infoWindow.setContent(this.html);
                infoWindow.open(map, this);
            });

        }

    });
  
}