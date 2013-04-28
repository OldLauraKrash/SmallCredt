$(document).ready(function(){
    // revert on login
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
    // include validate for forms
	$('#form-sign-up').validationEngine();
	$('#form-auth').validationEngine();
    $('#form-auth-main').validationEngine();


    // register
	$('#form-sign-submit').live("click", function(){

		if ($("#form-sign-up").validationEngine('validate')) {
            var jqxhr = $.getJSON('/register/', {'email': $('#form-sign-up-email').val(), 'password':$('#form-sign-up-confirm-password').val()} ,function(data) {
                if (data['result']=='ok') {
                    window.location.href = '/profile';
                } else {
                    $("#form-sign-submit").validationEngine('showPrompt', 'This email is busy', 'error');
                }
            }).fail(function() { $("#form-sign-submit").validationEngine('showPrompt', 'This email is busy', 'error'); });
		}
		return false;
	});

    // login
    $('#form-auth-main-submit').live("click", function(){
        if ($("#form-auth-main").validationEngine('validate')) {
            var jqxhr = $.getJSON('/login/', {'email': $('#form-auth-main-email').val(), 'password':$('#form-auth-main-password').val()} ,function(data) {
                if (data['result']=='ok') {
                    window.location.href = '/profile';
                }  else {
                    $("#form-auth-main-password").validationEngine('showPrompt', 'Your email doesn’t match your password', 'error');
                }
            }).fail(function() { $("#form-auth-main-password").validationEngine('showPrompt', 'Your email doesn’t match your password', 'error'); });

        }
        return false;
    });  

    $('#form-auth-submit').live("click", function(){
        if ($("#form-auth").validationEngine('validate')) {
            var jqxhr = $.getJSON('/login/', {'email': $('#form-auth-email').val(), 'password':$('#form-auth-password').val()} ,function(data) {
                if (data['result']=='ok') {
                    window.location.href = '/profile';
                }  else {
                   $("#form-auth-password").validationEngine('showPrompt', 'Your email doesn’t match your password', 'error');
                }
            }).fail(function() { $("#form-auth-password").validationEngine('showPrompt', 'Your email doesn’t match your password', 'error'); });
        }
        return false;
    });


    // include validate for forms profile
    $('#general-form-profile').validationEngine();
    $('#general-form-profile-business').validationEngine();
    $('#general-form-profile-credit').validationEngine();
    $('#form-password-reset').validationEngine();
    
    // save profile main
    $('#general-form-profile-submit').live("click", function(){
        $(this).parent().parent().fadeOut();
        if ($("#general-form-profile").validationEngine('validate')) {
            $.get('/save-profile-main/', $('#general-form-profile').serialize());
        }
        $(this).parent().parent().fadeIn();
        return false;
    });

    // save profile business
    $('#general-form-profile-business-submit').live("click", function(){
        $(this).parent().parent().fadeOut();
        if ($("#general-form-profile-business").validationEngine('validate')) {
            $.get('/save-profile-business/', $('#general-form-profile-business').serialize());
        }
        $(this).parent().parent().fadeIn();
        return false;
    });

    // save profile credit
    $('#general-form-profile-credit-submit').live("click", function(){
        $(this).parent().parent().fadeOut();
        if ($("#general-form-profile-credit").validationEngine('validate')) {
            $.get('/save-profile-credit/', $('#general-form-profile-credit').serialize());
        }
        $(this).parent().parent().fadeIn();
        return false;
    });

});