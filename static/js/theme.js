$(function () {
    $('#btn-swap-theme').on('click' ,function(event) {
        $(this).toggleClass('active');
        $('html').toggleClass('night');
    });
  });
