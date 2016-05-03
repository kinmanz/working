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
        var info = $(this).attr("data-info");
        var me = $(this);
        $.get('/rank/auto_add_page/', {category_id: catid, url: url, title: title, information : info }, function(data){
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
         $(this).hide();
         $('#change-form').show();


                        });

    $("#change-bth").click(function(){
        $('#change-form').show();
        var me = $(this);
        var inf = $("#change_information").val();
        var catid = $(this).attr("data-catid");

        $.get('/rank/change_category/', {cat_id: catid, information: inf}, function(data){
                    if (data == "ok" )
                    {
                        $("#cat-info").html(inf);
                        $('#change-form').hide();
                        $(".rank-change").show();

                    } else {
                        $("#change_information").attr("placeholder", data);
                    }
                        });
                        });

    $(".page-change-bth").click(function(){
        var me = $(this);
        //var info = $('#lock-info');
         me.hide();
        var pageid = me.attr("data-pageid");
        $("#change-form-page" + pageid).show();
    });

     $(".change-bth-page").click(function() {
         var me = $(this);
         var page_id = me.attr("data-pageid");
         var cat_id = me.attr("data-catid");

         var cur_selector = "change-form-page" + page_id;

         var inf = $("#" + "change_information_page" + page_id).val();
         $.get('/rank/change_page/', {page_id: page_id, cat_id: cat_id, information: inf}, function(data){
                    if (data == "ok" )
                    {
                        $("#page-info" + page_id).html(inf);
                        $("#" + cur_selector).hide();
                        $("#change-bth" + page_id).show();
                        $("#page-info" + page_id).addClass("well well-sm");

                    } else {
                        $("#" + "change_information_page" + page_id).attr("placeholder", data);
                    }
                        });
     });

    $(".delete-page").click(function() {
         var me = $(this);
         var page_id = me.attr("data-id");
         var page_li = $("#list-group-item" + page_id)

    $.get('/rank/delete_page/', {page_id: page_id}, function(data){
                    if (data == "ok" )
                    {
                        page_li.hide();

                    } else {
                        alert(data);
                    }
                        });
        });
});


