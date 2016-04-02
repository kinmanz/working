
$(document).ready( function() {

    //$("#likes").click( function(event) {
    //    alert("You clicked the button using JQuery!");
    //});

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
    //$('button').addClass('btn btn-primary')

    //$("#about-btn").click( function(event) {
    //    msgstr = $("#msg").html() //gethtml in element
    //    msgstr = msgstr + "o"
    //    $("#msg").html(msgstr) //set html in element
    //});
    $("#likes").click(function(){
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/rango/like_category/', {category_id: catid}, function(data){
               $('#like_count').html(data);
               $('#likes').hide();
    });
    });

    $('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/rango/suggest_category/', {suggestion: query}, function(data){
         $('#cats').html(data);
        });
    });

});