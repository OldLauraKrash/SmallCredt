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
    $('#general-form-profile-accepted').validationEngine();

    // accepted credit
    $('.accepted-credit').live("click", function(){
        window.location.href = '/profile/accepted';   
    });

    // register
	$('#form-sign-submit').live("click", function(){
		if ($("#form-sign-up").validationEngine('validate')) {
            var amount = $('.ui-slider-handle').html();
            amount = amount.substring(0,amount.length-1);
            var jqxhr = $.getJSON('/register/', {'email': $('#form-sign-up-email').val(), 'password':$('#form-sign-up-confirm-password').val(), 'amount':amount} ,function(data) {
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

    $('.active-user').live("click", function(){
        var amount = $('.ui-slider-handle').html();
        window.location.href = '/profile/?amount='+amount.substring(0,amount.length-1);
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
            $('.ui-datepicker').hide();
            $.get('/save-profile-main/', $('#general-form-profile').serialize());
            lineProgress();
            $('#general-form-profile-business-name-first').focus();
        }
        $(this).parent().parent().fadeIn();
        return false;
    });

    // save profile business
    $('#general-form-profile-business-submit').live("click", function(){
        $(this).parent().parent().fadeOut();
        if ($("#general-form-profile-business").validationEngine('validate')) {
            $('.ui-datepicker').hide();
            $.get('/save-profile-business/', $('#general-form-profile-business').serialize());
            lineProgress();
            $('#general-form-profile-credit-loan-amount').focus();
        }
        $(this).parent().parent().fadeIn();
        return false;
    });

    // save profile credit
    $('#general-form-profile-credit-submit').live("click", function(){
        $(this).parent().parent().fadeOut();
        if ($("#general-form-profile-credit").validationEngine('validate')) {
            $.get('/save-profile-credit/', $('#general-form-profile-credit').serialize(), function(data) {
                if (data.result == 'ok') {
                    if (lineProgress()==70) {
                       window.location.href = '/qualify';   
                    }
                }
            });
        }
        $(this).parent().parent().fadeIn();
        return false;
    });
    
    $('input[placeholder]').placeholder();

    function lineProgress() {

        if ($('.line-progress').css('width') == '689px')
            return 70;

        var width = 20;
        var countInput = 0;
        $( "#general-form-profile input" ).each(function( index ) {
            if ($(this).val()!="") 
                countInput++;
        });

        if (countInput > 10)
           width +=20; 

        var countInput = 0;
        $( "#general-form-profile-business input" ).each(function( index ) {
            if ($(this).val()!="") 
                countInput++;
        });
        if (countInput > 8)
           width +=20; 

        var countInput = 0;
        $( "#general-form-profile-credit input" ).each(function( index ) {
            if ($(this).val()!="") 
                countInput++;
        });
        if (countInput > 1)
           width +=10; 


        $('.line-progress').css('width', width+'%')            
        return width;
    }
    lineProgress();

    //$('#general-form-profile-date').datepicker({dateFormat: 'yy-mm-dd'});
    //$('#general-form-profile-business-legal-third').datepicker({dateFormat: 'yy-mm-dd'});

    // autocomplete
    var suffix = [
      "Mr.",
      "Ms.",
      "Mrs.",
      "Miss.",
      "Dr."
    ];
    $( "#general-form-profile-your-name-first" ).autocomplete({
      source: suffix,
      minLength: 0,
    }).focus(function(){            
        $(this).autocomplete("search");
    });


    $("#general-form-profile-business-legal-first").autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-legal-form",
            dataType: "json",
            data: {'term': $( "#general-form-profile-business-legal-first" ).val()},
            success: function( data ) {
                response( $.map( data.categories, function( item ) {
                    return {
                        label: item,
                        value: item
                    }
            }));
            }});
        },
        minLength: 0,
    }).focus(function(){            
        $(this).autocomplete("search");
    });

    $('#general-form-profile-business-address-third').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-state",
            dataType: "json",
            data: {'term': $('#general-form-profile-business-address-third').val()},
            success: function( data ) {
                response( $.map( data.categories, function( item ) {
                    return {
                        label: item,
                        value: item
                    }
            }));
        }});
        },
        minLength: 0,
    }).focus(function(){            
        $(this).autocomplete("search");
    });

    $('#general-form-profile-addresse-third').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-state",
            dataType: "json",
            data: {'term': $('#general-form-profile-addresse-third').val()},
            success: function( data ) {
                response( $.map( data.categories, function( item ) {
                    return {
                        label: item,
                        value: item
                    }
            }));
        }});
        },
        minLength: 0,
    }).focus(function(){            
        $(this).autocomplete("search");
    });

    $('#general-form-profile-addresse-country').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-country",
            dataType: "json",
            data: {'term': $('#general-form-profile-addresse-country').val()},
            success: function( data ) {
                response( $.map( data.categories, function( item ) {
                    return {
                        label: item,
                        value: item
                    }
            }));
        }});
        },
        minLength: 0,
    }).focus(function(){            
        $(this).autocomplete("search");
    });

    $('#general-form-profile-business-address-country').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-country",
            dataType: "json",
            data: {'term': $('#general-form-profile-business-address-country').val()},
            success: function( data ) {
                response( $.map( data.categories, function( item ) {
                    return {
                        label: item,
                        value: item
                    }
            }));
        }});
        },
        minLength: 0,
    }).focus(function(){            
        $(this).autocomplete("search");
    });

    $('.input-industry').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-industry",
            dataType: "json",
            data: {'term': $('.input-industry').val()},
            success: function( data ) {
                response( $.map( data.categories, function( item ) {
                    return {
                        label: item,
                        value: item
                    }
            }));
        }});
        },
        minLength: 0,
    }).focus(function(){        
        $(this).autocomplete("search");
    });

    $('#general-form-profile-business-legal-second').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-state",
            dataType: "json",
            data: {'term': $('.input-state').val()},
            success: function( data ) {
                response( $.map( data.categories, function( item ) {
                    return {
                        label: item,
                        value: item
                    }
            }));
        }});
        },
        minLength: 0,
    }).focus(function(){        
        $(this).autocomplete("search");
    });

    $('#form-accepted-first-file1, #form-accepted-first-file2, #form-accepted-first-file3').change(function() {
        $('#accepted-save-files').submit();
    });
});