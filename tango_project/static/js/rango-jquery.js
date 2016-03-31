$(document).ready( function() {

    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
    });

    //find classes
    //$(".ouch").click( function(event) {
    //       alert("You clicked me! ouch!");
    //});

    //$("p").hover( function() {
    //        $(this).css('color', 'red');
    //},
    //function() {
    //        $(this).css('color', 'blue');
    //});

    //$("#about-btn").addClass('btn btn-primary')

    //поставился для дефаулт кнопок
    //This will select the element with id #about-btn, and assign the classes btn and btn-primary to it.
    $('button').addClass('btn btn-primary')

    //$("#about-btn").click( function(event) {
    //    msgstr = $("#msg").html() //gethtml in element
    //    msgstr = msgstr + "o"
    //    $("#msg").html(msgstr) //set html in element
    //});
});


