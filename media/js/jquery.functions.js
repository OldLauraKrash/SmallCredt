$(document).ready(function(){
    $('.login-revert').live("click", function(){
        $(this).parents('.popup-holder').fadeOut(300, function(){
            $('.formError').remove();
            $('.popup-holder').css({"left": "-9999px"});
            $('.popup-holder').height(0);
            $('.popup-holder').show();

            popupbg();
            $('#popup3').css({"left": "-9999px"});
            $('#popup3').show();
            windowScroll($('#popup3 .popup').height());
            $('#popup3').hide();
            $('#popup3').css({"left": "0"});
            $('#popup3 .popup').css('top',wScroll);
            $('#popup3').fadeIn(200);
        });
    });


	$('#form-sign-up').validationEngine();
	$('#form-auth').validationEngine();
	$('#form-forget').validationEngine();

	$('#form-sign-submit').live("click", function(){
		if ($("#form-sign-up").validationEngine('validate')) {
            $.getJSON('/register/', {'email': $('#form-sign-up-email').val(), 'password':$('#form-sign-up-confirm-password').val()} ,function(data) {
                if (data['result']=='ok') {
                    $('.form-user').hide();
                    $('.welcom-block').show();
                    $('.welcome').html(data['username']);
                }
            });
            $(this).parents('.popup-holder').fadeOut(300, function(){
                $('.formError').remove();
                $('.popup-holder').css({"left": "-9999px"});
                $('.popup-holder').height(0);
                $('.popup-holder').show();
            });
		}
		return false;
	});

});