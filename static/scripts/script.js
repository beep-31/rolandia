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

    $('.form__dropdown').click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).toggleClass('form__dropdown--expanded');
        $('#'+$(e.target).attr('for')).prop('checked',true);
      });
      $(document).click(function() {
        $('.form__dropdown').removeClass('form__dropdown--expanded');
      });
    
});