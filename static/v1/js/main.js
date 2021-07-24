
var Api_Url = window.location.origin;

function get(url, callbackSuccess, callbackError) {
    complete_url = Api_Url + url;

    incrOngoingCallCount();
    $.get(complete_url, function(data) {
        console.log("[INFO] get", complete_url, data);
        decrOngoingCallCount();
        if (callbackSuccess) {
            callbackSuccess(data);
        }
    })
    .fail(function() {
        console.log("[ERROR] get", complete_url);
        decrOngoingCallCount();
        if (callbackError) {
            callbackError("");
        }
    });
}

function post(url, inputData, callbackSuccess, callbackError) {
    complete_url = Api_Url + url;
    payload = JSON.stringify(inputData);

    incrOngoingCallCount();
    $.ajax({
        type: "post",
        url: complete_url,
        data: payload,
        contentType: "application/json",  
        dataType: 'json', 
        success: function(data) {
            decrOngoingCallCount();
            if (data != null) {
                console.log("[INFO] post", complete_url, inputData, "response:", data);
                if (callbackSuccess) {
                    callbackSuccess(data);
                }
            }
            else {
                console.log("[ERROR] post", complete_url, inputData);
                if (callbackError) {
                    callbackError("");
                }
            }
        },
        fail: function(err) {
            decrOngoingCallCount();
            console.log("[FAIL] post", complete_url, inputData, "response", err);
            if (callbackError) {
                callbackError(err);
            }
        },
        error: function(err) {
            decrOngoingCallCount();
            console.log("[ERROR] post", complete_url, inputData, "response", err);
            if (callbackError) {
                callbackError(err.responseJSON);
            }
        },
    });
}

var dopostqueue = $({});
function sequentialPost(url, payload, callback)
{
    dopostqueue.queue(function()
    {
        $.ajax(
        {   
            type: 'POST',
            url: Api_Url + url,
            datatype: 'json',
            data: JSON.stringify(payload),
            success: function(result) 
            {
                console.log("[INFO] sequential post", Api_Url + url, payload, "response:", result);
                dopostqueue.dequeue();
                callback(result);
            }
        })
    });
}

var dogetqueue = $({});
function sequentialGet(url, callback)
{
    dogetqueue.queue(function()
    {
        $.ajax(
        {   
            type: 'GET',
            url: Api_Url + url,
            success: function(result) 
            {
                console.log("[INFO] sequential get", (Api_Url + url), "response:", result);
                dogetqueue.dequeue();
                callback(result);
            }
        })
    });
}

function refreshGameRoom() {
    get("/api/v1/" + getLoadGameRoomOwnerToJoin() + "/gamerooms/" + getLoadGameRoomNameToJoin(), function(data) {
        setParticipants(data["participants"].join(","));
    }, function(err) {
        alert("Gameroom refresh failed " + err);
    });
}

var adminMode = null;
function toggleAdmin() {
    adminMode = !adminMode;
    if (adminMode) {
        $(".adminBlock").show();
    }
    else {
        $(".adminBlock").hide();
    }
}


function updateGameStatus(status) {
    $("#txtGameStatus").html(status);
}

function updateGameWinners(winner_list) {
    $("#txtGameWinners").html(winner_list.length > 0 ? winner_list.join(", ") : "N/A");
}

function updateGameParticipantSequence(participants_index_id_map, whose_turn_index, forward_direction) {
    var activePlayerTemplate = '<span style="color: red;">({{username}})</span>';
    var normalPlayerTemplate = "{{username}}";

    var tagsList = [];
    for (var participantIdx in participants_index_id_map) {
        var val = normalPlayerTemplate;
        if (whose_turn_index == participantIdx) {
            val = activePlayerTemplate;
        }
        val = val.replace("{{username}}", participants_index_id_map[participantIdx]);
        tagsList.push(val);
    }

    $("#txtParticipantsSequence").html(forward_direction ? tagsList.join(" -> ") : tagsList.join(" <- "));
}

function updateGameCurrentColor(color) {
    var r = '<span style="background: red;">&nbsp;&nbsp;&nbsp;&nbsp;</span>';
    var g = '<span style="background: green;">&nbsp;&nbsp;&nbsp;&nbsp;</span>';
    var b = '<span style="background: blue;">&nbsp;&nbsp;&nbsp;&nbsp;</span>';
    var y = '<span style="background: yellow;">&nbsp;&nbsp;&nbsp;&nbsp;</span>';

    if (color == 'r') {
        $("#txtCurrentColor").html(r);
    }
    else if (color == 'g') {
        $("#txtCurrentColor").html(g);
    }
    else if (color == 'b') {
        $("#txtCurrentColor").html(b);
    }
    else if (color == 'y') {
        $("#txtCurrentColor").html(y);
    }
}


// TODO Specify change color to 

function getGameColorChoice() {
    return $("#selectNewColor").val();
}

function cardCallback(unique_id, is_wild) {
    var change_color_to = "";
    if (is_wild) {
        var result = confirm("Are you sure with color choice: " + getGameColorChoice());
        if (result) {
            change_color_to = getGameColorChoice();
        }
        else {
            return;
        }
    }

    post("/api/v1/games/" + getGameIdToJoinGame() + "/process", {
        "username": getUsernameForLogin(),
        "plays_card_uid": unique_id,
        "declares_last_card": false,
        "change_color_to": change_color_to
    }, function(data) {
        alert("Card played successfully ");
        updateGameModel(data);
    }, function(err) {
        alert("Card playing failed ");
        updateGameModel(err);
    });
}

function callLastCard() {
    post("/api/v1/games/" + getGameIdToJoinGame() + "/process", {
        "username": getUsernameForLogin(),
        "plays_card_uid": "",
        "declares_last_card": true,
        "change_color_to": ""
    }, function(data) {
        alert("Calling last card success ");
        updateGameModel(data);
    }, function(err) {
        alert("Calling last card failed " + err);
        updateGameModel(err);
    });
}

function updateGameCard(cards_sequence, cards_uid_index_map, user_card_uid_list) {
    var cardTemplate = '<div class="card-des card-{{color}}" card-id="{{card-id}}" onclick="cardCallback(\'{{card-id}}\', {{is-wild}});">{{text}}</div>';
    var tagList = [];
    var userCards = [];
    for (var card_uid of user_card_uid_list) {
        var idx = cards_uid_index_map[card_uid];
        var card = cards_sequence[idx];
        userCards.push(card);

        var number = card.number.toString();
        if (card.is_draw_2) number = "+2";
        if (card.is_draw_4) number = "+4";
        if (card.is_reverse) number = "rev- erse";
        if (card.is_skip) number = "skip";
        if (number == "-1") number = "chg. color";
        
        var color = card.is_wild ? "w" : card.color;
        var val = cardTemplate.replace("{{color}}", color).replace("{{text}}", number);
        val = val.replace("{{card-id}}", card.unique_id);
        val = val.replace("{{card-id}}", card.unique_id);
        val = val.replace("{{is-wild}}", card.is_wild.toString());
        tagList.push(val);
    }
    $("#divUserCardList").html(tagList.join(""));
    console.log("User cards", userCards);
}

function updateWithDummyGameCards() {
    var cardTemplate = '<div class="card-des card-{{color}}" card-id="{{card-id}}" onclick="cardCallback(\'{{card-id}}\', {{is-wild}});">{{text}}</div>';
    var tagList = [];
    var userCards = [];
    var user_card_list = [
        {unique_id: "", is_wild: false, color: 'r'},
        {unique_id: "", is_wild: false, color: 'g'},
        {unique_id: "", is_wild: false, color: 'b'},
        {unique_id: "", is_wild: false, color: 'y'}
    ];
    for (var card of user_card_list) {
        userCards.push(card);

        var number = 0;
        var color = card.is_wild ? "w" : card.color;
        var val = cardTemplate.replace("{{color}}", color).replace("{{text}}", number);
        val = val.replace("{{card-id}}", card.unique_id);
        val = val.replace("{{card-id}}", card.unique_id);
        val = val.replace("{{is-wild}}", card.is_wild.toString());
        tagList.push(val);
    }
    $("#divUserCardList").html(tagList.join(""));
    console.log("User cards", userCards);
}

function updateWithWinnerGameCards() {
    var color_list = ['r', 'g', 'b', 'y', 'w'];
    var cardTemplate = '<div class="card-des card-{{color}}" card-id="{{card-id}}" onclick="cardCallback(\'{{card-id}}\', {{is-wild}});">{{text}}</div>';
    var tagList = [];
    var userCards = [];
    var user_card_list = [
        {unique_id: "", is_wild: false, number: 'W'},
        {unique_id: "", is_wild: false, number: 'I'},
        {unique_id: "", is_wild: false, number: 'N'},
        {unique_id: "", is_wild: false, number: 'N'},
        {unique_id: "", is_wild: false, number: 'E'},
        {unique_id: "", is_wild: false, number: 'R'}
    ];
    for (var card of user_card_list) {
        userCards.push(card);

        var number = card.number.toString();
        var color = color_list[Math.floor(Math.random()*color_list.length)];;
        var val = cardTemplate.replace("{{color}}", color).replace("{{text}}", number);
        val = val.replace("{{card-id}}", card.unique_id);
        val = val.replace("{{card-id}}", card.unique_id);
        val = val.replace("{{is-wild}}", card.is_wild.toString());
        tagList.push(val);
    }
    $("#divUserCardList").html(tagList.join(""));
    console.log("User cards", userCards);
}

function updateGameDeckCount(deck_count) {
    $("#txtGameDeckCount").html(deck_count);
}

function updateUsersWithLastCard(last_card_people_map) {
    var userlist = [];
    for (var uid in last_card_people_map)
        userlist.push(uid);
    $("#txtUsersWithLastCard").html(userlist.length > 0 ? userlist.join(", ") : "N/A");
}

function updateGameLastCard(cards_sequence) {
    var cardTemplate = '<div class="card-des card-{{color}}" card-id="{{card-id}}" onclick="cardCallback(\'{{card-id}}\', {{is-wild}});">{{text}}</div>';
    if (cards_sequence.length == 0) return;

    var idx = cards_sequence.length - 1;
    var card = cards_sequence[idx];

    var number = card.number.toString();
    if (card.is_draw_2) number = "+2";
    if (card.is_draw_4) number = "+4";
    if (card.is_reverse) number = "rev- erse";
    if (card.is_skip) number = "skip";
    if (number == "-1") number = "chg. color";
    
    var color = card.is_wild ? "w" : card.color;
    var val = cardTemplate.replace("{{color}}", color).replace("{{text}}", number);
    val = val.replace("{{card-id}}", card.unique_id);
    val = val.replace("{{card-id}}", card.unique_id);
    val = val.replace("{{is-wild}}", card.is_wild.toString());
    
    $("#divGameLastCard").html(val);
    console.log("Last card", card);
}

function updateLastCardPlayedBy(participants_played_sequence) {
    if (participants_played_sequence.length == 0) return;
    var participant = participants_played_sequence[participants_played_sequence.length - 1];
    $("#txtLastCardPlayedBy").html(participant);
}

function updateGameModel(gameModel) {
    if (getUsernameForLogin() in gameModel.participants_id_cards_map) {
        updateGameCard(gameModel.cards_sequence, gameModel.cards_uid_index_map, gameModel.participants_id_cards_map[getUsernameForLogin()]);
    }
    else if (gameModel.winner_id_list.includes(getUsernameForLogin())) {
        updateWithWinnerGameCards();
    }
    else {
        updateWithDummyGameCards();
    }

    updateLastCardPlayedBy(gameModel.participants_played_sequence);
    updateGameLastCard(gameModel.cards_played_sequence);
    updateGameStatus(gameModel.game_ended ? "FINISHED": "UNFINISHED");
    updateGameWinners(gameModel.winner_id_list);
    updateGameParticipantSequence(gameModel.participants_index_id_map, gameModel.whose_turn_index, gameModel.forward_direction);
    updateGameCurrentColor(gameModel.current_color);
    updateGameDeckCount(gameModel.deck_count);
    updateUsersWithLastCard(gameModel.last_card_people_map);
}



function getUsernameForLogin() {
    return $("#txtUsername").val();
}

function getGameRoomNameToCreate() {
    return $("#txtCreateGameRoom").val();
}

function getGameRoomPasscodeToCreate() {
    return $("#txtCreateGameRoomPasscode").val();
}

function setLoadGameRoomName(name) {
    $("#txtLoadGameRoomName").val(name);
}

function setLoadGameRoomPasscode(pass) {
    $("#txtLoadGameRoomPasscode").val(pass);
}




function getLoadGameRoomOwnerToJoin() {
    return $("#txtLoadGameRoomOwner").val();
}

function setLoadGameRoomOwnerToJoin(val) {
    $("#txtLoadGameRoomOwner").val(val);
}

function getLoadGameRoomNameToJoin() {
    return $("#txtLoadGameRoomName").val();
}



function setParticipants(val) {
    $("#txtParticipants").html(val);
}



function getDeckCountToStartGame() {
    return $("#txtDeckCount").val();
}





function getGameIdToJoinGame() {
    return $("#txtGameId").val();
}




function incrOngoingCallCount() {
    var val = $("#txtOngoingCallCount").html();
    val = parseInt(val) + 1;
    $("#txtOngoingCallCount").html(val.toString());
}

function decrOngoingCallCount() {
    var val = $("#txtOngoingCallCount").html();
    val = parseInt(val) - 1;
    $("#txtOngoingCallCount").html(val.toString());
}


var autoRefreshDelay = 5000;
function getGameRecursive() {
    sequentialGet("/api/v1/games/" + getGameIdToJoinGame(), function(data) {
        if (data != null)
            updateGameModel(data);
        // getGameRecursive();
        setTimeout(getGameRecursive, autoRefreshDelay);
    });
}

$(document).ready(function() {

    $(".adminBlock").hide();
    adminMode = false;

    $("#btnLogin").click(function() {
        post('/api/login', {
            "username": getUsernameForLogin(),
            "passcode": "1234"
        }, function(data) {
            alert("Login success");
        }, function(err) {
            alert("Failed to login " + err);
        });
    });

    $("#btnCreateGameRoom").click(function() {
        var gameRoomName = getGameRoomNameToCreate();
        var gameRoomPasscode = getGameRoomPasscodeToCreate();
        if (gameRoomName != null) {
            post('/api/v1/' + getUsernameForLogin() + '/gamerooms', {
                "gameroom_name": gameRoomName,
                "password": gameRoomPasscode
            }, function(data) {
                alert("Gameroom creation success");
                setLoadGameRoomName(data["name"]);
                setLoadGameRoomPasscode(data["password"]);
                setLoadGameRoomOwnerToJoin(getUsernameForLogin());
            }, function(err) {
                alert("Gameroom creation failed " + err)
            })
        }
        else {
            alert("No gameroom created");
        }
    });

    $("#btnLoadGameRoom").click(function() {
        post("/api/v1/" + getLoadGameRoomOwnerToJoin() + "/gamerooms/" + getLoadGameRoomNameToJoin() + "/adduser", {
            "username": getUsernameForLogin()
        }, function(data) {
            alert("Gameroom joining success " + data);
            refreshGameRoom();
        }, function(err) {
            alert("Gameroom joining failed " + err);
        });
    });

    $("#btnRefreshGameRoom").click(function() {
        refreshGameRoom();
    });

    $("#btnToggleAdmin").click(function() {
        toggleAdmin();
    });

    $("#btnStartGame").click(function() {
        post("/api/v1/" + getLoadGameRoomOwnerToJoin() + "/gamerooms/" + getLoadGameRoomNameToJoin() + "/start", {
            "deck_count": getDeckCountToStartGame()
        }, function(data) {
            alert("Game creation success ");
            refreshGameRoom();
        }, function(err) {
            alert("Game creation failed " + err);
        });
    });

    $("#btnJoinGame").click(function() {
        get("/api/v1/games/" + getGameIdToJoinGame(), function(data) {
            alert("Game joining success");
            updateGameModel(data);
        }, function(err) {
            alert("Game joining failed " + err);
        });
    });

    getGameRecursive();

    $("#btnCallLastCard").click(callLastCard);
});
