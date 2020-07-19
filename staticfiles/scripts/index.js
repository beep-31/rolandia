$(document).ready(function(){
    $("#search_icon").click(function(){
        $("#searchbox").toggleClass('search-input--active');
    });

    $("#burger").click(function(){
        $("#nav__mobile").animate({
            left: "0%"
        }, 300);
    });
    
    $("#nav__close").click(function(){
        $("#nav__mobile").animate({
            left: "-100%"
        }, 300); 
    });
});