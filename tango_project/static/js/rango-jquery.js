$(document).ready( function() {

    //$("#about-btn").click( function(event) {
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
//    $("#likes").click(function(){
//    var catid;
//    catid = $(this).attr("data-catid");
//    $.get('/rango/like_category/', {category_id: catid}, function(data){
//               $('#like_count').html(data);
//               $('#likes').hide();
//    });
//});
    $('.rango-add').click(function(){
    var catid = $(this).attr("data-catid");
        var url = $(this).attr("data-url");
        var title = $(this).attr("data-title");
        var me = $(this);
        $.get('/rank/auto_add_page/', {category_id: catid, url: url, title: title}, function(data){
                        $('#pages').html(data);
                        me.hide();
                        });
                                });
    $(".lock-btn").click(function(){
        var me = $(this);
        var catid = $(this).attr("data-catid");
        $.get('/rank/lock/', {category_id: catid}, function(data){
                    if (me.html() == "Lock" )
                    {
                        me.html("Unlock");
                    } else {
                        me.html("Lock");
                    }
                    $('#lock-info').html(data);
                        });
                                });

    $(".rank-change").click(function(){
        var me = $(this);
        //var info = $('#lock-info');
         $('#cat-info').html("aaaa --------------------- ");
                        });
});


