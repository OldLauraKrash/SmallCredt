$(document).ready(function(){

    // change status type password
    if ($.browser.msie  && parseInt($.browser.version, 10) === 8) {
      $('[type=password]').removeAttr('placeholder');
      $('[type=password]').val('Password');
      $('[type=password]').attr('rel', 'Password');
      $('[type=password]').addClass('ie-password');      
    }

    // placeholder for ie
    $(".ie-password").live('focus', function() {
       if ($(this).val()=='') {
        $(this).val('Password');
       }
       if ($(this).val()==$(this).attr('rel')) {
         $(this).val('');
       }       
    });

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
    $('#lender-form').validationEngine();

    // accepted credit
    $('.accepted-credit').live("click", function(){
        $(location).attr('href', '/profile/accepted/');  
    });

    // register
	$('#form-sign-submit').live("click", function(){
		if ($("#form-sign-up").validationEngine('validate')) {
            var amount = $('.ui-slider-handle').html();
            amount = amount.substring(0,amount.length-1);
           $.get('/register/', {'email': $('#form-sign-up-email').val(), 'password':$('#form-sign-up-confirm-password').val(), 'amount':amount} ,function(data) {
                if (data['result']=='ok') {
                    $(location).attr('href', '/profile');
                } else {
                    $("#form-sign-submit").validationEngine('showPrompt', 'This account already exists', 'error');
                }
            }).fail(function() { $("#form-sign-submit").validationEngine('showPrompt', 'This account already exists', 'error'); });
		}
		return false;
	});

    // login
    $('#form-auth-main-submit').live("click", function(){
        if ($("#form-auth-main").validationEngine('validate')) {
            $.get('/login/', {'email': $('#form-auth-main-email').val(), 'password':$('#form-auth-main-password').val()} ,function(data) {
                if (data['result']=='ok') {
                    if (data['lender'])
                        $(location).attr('href', '/lender/account/');
                    else
                        $(location).attr('href', '/profile');
                }  else {
                    $("#form-auth-main-password").validationEngine('showPrompt', 'Sorry, wrong password :(', 'error');
                }
            }).fail(function() { $("#form-auth-main-password").validationEngine('showPrompt', 'Sorry, wrong password :(', 'error'); });

        }
        return false;
    });  

    // auth form
    $('#form-auth-submit').live("click", function(e){
        if ($("#form-auth").validationEngine('validate')) {
            e.preventDefault();
            $.get('/login/', {'email': $('#form-auth-email').val(), 'password':$('#form-auth-password').val()} ,function(data) {
                if (data['result']=='ok') {
                    if (data['lender'])
                        window.location.href = '/lender/account/';
                    else
                        window.location.href = '/profile';
                }  else {
                   $("#form-auth-password").validationEngine('showPrompt', 'Sorry, wrong password :(', 'error');
                }
            }).fail(function() { $("#form-auth-password").validationEngine('showPrompt', 'Sorry, wrong password :(', 'error'); });
        }
        return false;
    });

    // active user
    $('.active-user').live("click", function(){
        var amount = $('.ui-slider-handle').html();
        window.location.href = '/profile/?amount='+amount.substring(0,amount.length-1);
    });

    // bid 
    $('#bid').live("click", function(){
        $('.link-holder').hide();
        $.get('/lender/marketplace/bid/', { 'id': $(this).attr('rel'), 
                                            'amount': $('#bid-amount').val(), 
                                            'discount': $('#bid-discount').val(),
                                            'daily': $('#bid-daily-repayment').val(),                                             
                                        }, function(data) {
            if (data.result == 'ok') {
                $('.link-holder').hide();
                var today = new Date();
                var dd = today.getDate();
                var mm = today.getMonth()+1; //January is 0!
                var yyyy = today.getFullYear();
                if(dd<10){dd='0'+dd} if(mm<10){mm='0'+mm} today = mm+'/'+dd+'/'+yyyy;
                $('.finish-date').html('You submitted <br/> your offer <br/> on '+today);
                $('.finish-date').append('<a href="#" class="change-bid" rel="'+data.id+'">Change bid</a>');
            }
        });
        return false;
    });

    // decline
    $('#decline').live("click", function(){
        $('.link-holder').hide();
        $.get('/lender/marketplace/decline/', { 'id': $(this).attr('rel') }, function(data) {
            if (data.result == 'ok') {
                $('.link-holder').hide();
                var today = new Date();
                var dd = today.getDate();
                var mm = today.getMonth()+1; //January is 0!
                var yyyy = today.getFullYear();
                if(dd<10){dd='0'+dd} if(mm<10){mm='0'+mm} today = mm+'/'+dd+'/'+yyyy;
                $('.finish-date').html('You declined <br/> on <br/> '+today);
                $('.finish-date').append('<a href="#" class="change-bid" rel="'+data.id+'">Change bid</a>');
            }
        });
        return false;
    });


    // include validate for forms profile
    $('#form-password-reset').validationEngine();
    
    // save profile main
    $('#general-form-profile-submit').live("click", function(){
        $('#general-form-profile').validationEngine();
        $(this).parent().parent().fadeOut();
        if ($.browser.msie  && parseInt($.browser.version, 10) === 8 || $.browser.msie  && parseInt($.browser.version, 10) === 9) {
        	$( "#general-form-profile input" ).each(function( index ) {
			  if ($(this).val() == $(this).attr('placeholder')) {
				  $(this).val('');
			  }
			});
        	
        } 
        if ($("#general-form-profile").validationEngine('validate')) {
            $.get('/save-profile-main/', $('#general-form-profile').serialize(), function(data) {
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

    // cancel bid
    $('.change-bid').live("click", function(){
        $.get('/loan/cancel/', {'id': $(this).attr('rel')}, function(data) {
            if (data.result == 'ok') {
                window.location.href = window.location.pathname
            }
        });
    }); 

    // finish alert
    $('.finish-button').live("click", function(){
        $.get('/account-finish/', function(data) {
            if (data.result == 'ok') {
                window.location.href = '/account/finish';
            }
        });
        return false;
    });

    // lender info
    $('.lender').live("click", function(){
        window.location.href = '/lender/info/'+$(this).attr('rel');
        return false;
    });

    // submit lender save
    $('#lender-form-submit').live("click", function(){
        $(this).parent().parent().fadeOut();
        if ($.browser.msie  && parseInt($.browser.version, 10) === 8 || $.browser.msie  && parseInt($.browser.version, 10) === 9) {
        	$( "#lender-form input" ).each(function( index ) {
			  if ($(this).val() == $(this).attr('placeholder')) {
				  $(this).val('');
			  }
			});
        	
        } 
        if ($("#lender-form").validationEngine('validate')) {
            $.get('/save-lender/', $('#lender-form').serialize(), function(data) {
                if (data.result == 'ok') {
                window.location.href = '/lender/account/';
                }
            });
        }
        $(this).parent().parent().fadeIn();
        return false;
    });

    // remove item tags
    $('.remove-item-list').live("click", function(){
        $.get('/lender/remove-item-tag/', {'id': $(this).parent().attr('rel'), 'type': $(this).attr('rel')}, function(data) {       
        });       
        $(this).parent().remove(); 
        return false;
    });

    // save profile business
    $('#general-form-profile-business-submit').live("click", function(){
        $('#general-form-profile-business').validationEngine();
        $(this).parent().parent().fadeOut();
        if ($.browser.msie  && parseInt($.browser.version, 10) === 8 || $.browser.msie  && parseInt($.browser.version, 10) === 9) {
        	$( "#general-form-profile-business input" ).each(function( index ) {
			  if ($(this).val() == $(this).attr('placeholder')) {
				  $(this).val('');
			  }
			});
        	
        }    
        if ($("#general-form-profile-business").validationEngine('validate')) {
            $('#general-form-profile-credit').fadeIn();
            $.get('/save-profile-business/', $('#general-form-profile-business').serialize(), function(data) {
                if (data.result == 'ok') {
                    lineProgress();
                    $('#general-form-profile-credit-loan-amount').focus();
                }
            });
        }
        $('#general-form-profile-credit-loan-amount').focus();
        $(this).parent().parent().fadeIn();
        return false;
    });

    // client id 
    $('.client').live("click", function(){
        window.location.href = '/lender/marketplace/borrower/'+$(this).attr('rel');
    });

    // accepted loan
    $('.accepted-loan').live("click", function(){
        $.get('/loan/accepted/', {'id': $(this).attr('rel')}, function(data) {
        });
        $(this).closest('.link-holder').hide();
        $(this).closest('.link-holder').next().removeClass('delete').addClass('normal').show();
        return false;
    });    

    // decline loan
    $('.decline-loan').live("click", function(){
        $.get('/loan/decline/', {'id': $(this).attr('rel')}, function(data) {
        });
        $(this).closest('.link-holder').hide();
        $(this).closest('.link-holder').next().removeClass('normal').addClass('delete').show();
        return false;
    });   

    // save profile credit
    $('#general-form-profile-credit-submit').live("click", function(){
        $('#general-form-profile-credit').validationEngine();
        $('.ui-menu-item').hide();
        $(this).parent().parent().fadeOut();
        if ($.browser.msie  && parseInt($.browser.version, 10) === 8) {
        	$( "#general-form-profile-credit input" ).each(function( index ) {
			  if ($(this).val() == $(this).attr('placeholder')) {
				  $(this).val('');
			  }
			});
        	
        } 
        if ($("#general-form-profile-credit").validationEngine('validate')) {
            $('#general-form-profile').fadeIn();
            $.get('/save-profile-credit/', $('#general-form-profile-credit').serialize(), function(data) {
                lineProgress();
                $('#general-form-profile-your-name-first').focus();
            });
        }
        $(this).parent().parent().fadeIn();
        return false;
    });

    // on placeholder    
    $('input[placeholder]').placeholder();

    // calculate line progress
    function lineProgress() {
        var width = 20;
        var countInput = 0;

        if ($('#general-form-profile-accepted').html() != undefined) {
          width = 70;  
        }

        $( "#general-form-profile input" ).each(function( index ) {
            if ($(this).focus().val()!="")
                countInput++;
            $('.ui-autocomplete').hide();                
        });

        if (countInput > 10)
           width +=20; 

        var countInput = 0;
        $( "#general-form-profile-business input" ).each(function( index ) {
            if ($(this).focus().val()!="") 
                countInput++;
            $('.ui-autocomplete').hide();
        });
        if (countInput > 8)
           width +=20; 

        var countInput = 0;
        $( "#general-form-profile-credit input" ).each(function( index ) {
            if ($(this).focus().val()!="")
                countInput++;
            $('.ui-autocomplete').hide();
        });
        if (countInput > 1)
           width +=10; 


        if ($('#accepted-save-files .list-files').html() != undefined) {

            if ($('#accepted-save-files .list-files').eq(0).find('li').length > 2)         
                width +=10;

            if ($('#accepted-save-files .list-files').eq(1).find('li').length > 2)      
                width +=10;

            if ($('#form-accepted-first-ein').val()!= undefined)
                width +=10;
        }

        $('.line-progress').css('width', width+'%')  

        if (width==100)
            $('.finish-button').show();

        return width;
    }
    lineProgress();


    //$('#general-form-profile-date').datepicker({dateFormat: 'yy-mm-dd'});
    //$('#general-form-profile-business-legal-third').datepicker({dateFormat: 'yy-mm-dd'});

    // autocomplete title
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

    var suffix = [
      "Mr.",
      "Ms.",
      "Mrs.",
      "Miss.",
      "Dr."
    ];
    $( "#lender-form-suffix" ).autocomplete({
      source: suffix,
      minLength: 0,
    }).focus(function(){            
        $(this).autocomplete("search");
    });

    // autocomplete legal
    $("#general-form-profile-business-legal-first").autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-legal-form/",
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

    // autocomplete state
    $('#general-form-profile-business-address-third').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-state/",
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

    // autocomplete state
    $('#general-form-profile-addresse-third').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-state/",
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

    $('#search-bank').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/api/get-institution/s",
            dataType: "json",
            data: {'term': $('#search-bank').val()},
            success: function( data ) {
                response( $.map( data.categories, function( item ) {
                    return {
                        label: item,
                        value: item
                    }
            }));
        }});
        },
        select: function( event, ui ) {
            $(location).attr('href','/api/connect/second/');
        },
        minLength: 0,
    }).focus(function(){
    });


    // autocomplete country
    $('#general-form-profile-addresse-country').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-country/",
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

    // autocomplete country
    $('#general-form-profile-business-address-country').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-country/",
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

    // autocomplete industry
    $('.input-industry').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-industry/",
            dataType: "json",
            data: {'term': $('.input-industry').val()},
            success: function( data ) {
                response( $.map( data.categories, function( item ) {                    
                    return {
                        label: item,
                        value: item
                    }
            }))}
             })
        },
        select: function( event, ui ) {
            $.get('/lender/save-tag/', {'type':'industry', 'name': ui.item.label}, function(data) {
                if (data.result == 'ok') {
                    $('.industry-list').append(' '+ui.item.label+' <a href="#" class="remove-item-list">[x]</a>');
                }
            });
        },
        minLength: 0,
    }).focus(function(){        
        $(this).autocomplete("search");
    });

    // autocomplete risk-level
    $('.input-risk-level').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-risk-level/",
            dataType: "json",
            data: {'term': $('.input-risk-level').val()},
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

    // autocomplete risk lender
    $('.input-risk').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-risk-lender/",
            dataType: "json",
            data: {'term': $('.input-risk').val()},
            success: function( data ) {
                response( $.map( data.categories, function( item ) {
                    return {
                        label: item,
                        value: item
                    }
            }));
        }});
        },
        select: function( event, ui ) {
            $('.input-risk').val('');
            $.get('/lender/save-tag/', {'type':'risk', 'name': ui.item.label}, function(data) {
                if (data.result == 'ok') {
                    $('.risk-level-list').append(' '+ui.item.label+' <a href="#" class="remove-item-list">[x]</a>');
                }
            });
        },
        minLength: 0,
    }).focus(function(){        
        $(this).autocomplete("search");
    });

    // autocomplete geography
    $('.input-geography').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-geography/",
            dataType: "json",
            data: {'term': $('.input-geography').val()},
            success: function( data ) {
                response( $.map( data.categories, function( item ) {
                    return {
                        label: item,
                        value: item
                    }
            }));
        }});
        },
        select: function( event, ui ) {
            $.get('/lender/save-tag/', {'type':'geography', 'name': ui.item.label}, function(data) {
                if (data.result == 'ok') {
                    $('.geography-list').append(' '+ui.item.label+' <a href="#" class="remove-item-list">[x]</a>');
                }
            });
        },
        minLength: 0,
    }).focus(function(){        
        $(this).autocomplete("search");
    });

    // autocomplete state
    $('#general-form-profile-business-legal-second').autocomplete({
        source: function( request, response ) {
        $.ajax({
            url: "/get-state/",
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

    function validateSize(fileInput) {
      var fileObj, size;
      if ( typeof ActiveXObject == "function" ) { // IE
        //fileObj = (new ActiveXObject("Scripting.FileSystemObject")).getFile(fileInput.value);
        return true;
      }else {
        fileObj = fileInput.files[0];
      }
     
      size = fileObj.size; // Size returned in bytes.
      if(size > 1 * 1024 * 1024){
        //fileInput.parentNode.innerHTML = fileInput.parentNode.innerHTML;
        return false;
      }
      return true;
    }

    // file upload
    $('#form-accepted-first-file1, #form-accepted-first-file2, #form-accepted-first-file3').change(function(e) {
        e.preventDefault();
        filename = $(this).val();
        filename = filename.split('.')[filename.split('.').length-1];
        filename = filename.toLowerCase();
        arr = [ "docx", "pdf", "jpeg", "png", "xls", "xlsx", "csv", "zip", "rtf", "txt", "doc", "jpg"];
        if (jQuery.inArray(filename, arr) == -1) {
            $('.error-extension').eq($(this).attr('rel')).show();
            return false;
        } else {
            $('.error-extension').eq($(this).attr('rel')).hide();            
        }

        if (validateSize(this)) {
            $('.error-file').eq($(this).attr('rel')).hide();
            $('#accepted-save-files').submit();
        } else {
            $('.error-file').eq($(this).attr('rel')).show();
        }
    });

    // targer
    var pathname = $(window.parent.location).attr('href');
    if (pathname.split('/')[4] == 'accepted') {
        class_name = '.'+pathname.split('#')[1];
        $('html,body').animate({
        scrollTop: $(class_name).offset().top},
        'slow');
    }


});
