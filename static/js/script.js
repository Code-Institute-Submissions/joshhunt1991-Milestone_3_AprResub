/*
    jQuery for MaterializeCSS initialization
*/

$(document).ready(function () {
    $(".sidenav").sidenav({edge: "right"});
    $('.carousel').carousel();

// function for automatic recent review image slider

    setInterval(function(){
        $('.carousel').carousel('next');

    }, 2500);
});



