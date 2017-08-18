$(function(){
    $("#Monday-button").click(function() {
        clear();
        $("#Monday").css("display", "block");
    });
    $("#Tuesday-button").click(function() {
        clear();
        $("#Tuesday").css("display", "block");
    });
    $("#Wednesday-button").click(function() {
        clear();
        $("#Wednesday").css("display", "block");
    });
    $("#Thursday-button").click(function() {
        clear();
        $("#Thursday").css("display", "block");
    });
    $("#Friday-button").click(function() {
        clear();
        $("#Friday").css("display", "block");
    });
    $("#Saturday-button").click(function() {
        clear();
        $("#Saturday").css("display", "block");
    });
    $("#Sunday-button").click(function() {
        clear();
        $("#Sunday").css("display", "block");
    });
    
});

function clear() {
    $("#Monday").css("display", "none");
    $("#Tuesday").css("display", "none");
    $("#Wednesday").css("display", "none");
    $("#Thursday").css("display", "none");
    $("#Friday").css("display", "none");
    $("#Saturday").css("display", "none");
    $("#Sunday").css("display", "none");
}