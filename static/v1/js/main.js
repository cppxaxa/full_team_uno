
var Api_Url = window.location.origin;

function get(url, callbackSuccess, callbackError) {
    complete_url = Api_Url + url;

    $.get(complete_url, function(data) {
        console.log("[INFO] get", complete_url, data);
        if (callbackSuccess) {
            callbackSuccess(data);
        }
    })
    .fail(function() {
        console.log("[ERROR] get", complete_url);
        if (callbackError) {
            callbackError("");
        }
    });
}

function post(url, inputData, callbackSuccess, callbackError) {
    complete_url = Api_Url + url;
    payload = JSON.stringify(inputData);

    $.ajax({
        type: "post",
        url: complete_url,
        data: payload,
        contentType: "application/json",  
        dataType: 'json', 
        success: function(data) {
            if (data != null) {
                console.log("[INFO] post", complete_url, data);
                if (callbackSuccess) {
                    callbackSuccess(data);
                }
            }
            else {
                console.log("[ERROR] post", complete_url);
                if (callbackError) {
                    callbackError("");
                }
            }
        },
        fail: function(err) {
            console.log("[ERROR] post", complete_url);
            if (callbackError) {
                callbackError(err);
            }
        }
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
});
