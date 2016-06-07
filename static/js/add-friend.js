"use strict";

function showSentRequest(result) {
    $("#add-friend-btn").html(result).attr("disabled", true);
}

function sendFriendRequest(evt) {
    evt.preventDefault();

    var formInput = {
        "user_b_id": $("#user-info").data("userid")
    };

    $.post("/add-friend",
           formInput,
           showSentRequest
           );
}

$("#add-friend-form").on("submit", sendFriendRequest);