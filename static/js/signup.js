$(document).ready(function(c) {
	$('.alert-close').on('click', function(c){
		$('.message').fadeOut('slow', function(c){
	  		$('.message').remove();
		});
	});	  

    var submit_form = function(e) {
    	if($('input[name="email"]').val() != "" && $('input[name="username"]').val() != "" && $('input[name="password"]').val() != "" && $('input[name="comfirmpassword"]').val() != "") {
      		$.post($SCRIPT_ROOT + '/signup', {
        		email: $('input[name="email"]').val(),
        		username: $('input[name="username"]').val(),
        		password: $('input[name="password"]').val(),
        		comfirmpassword: $('input[name="comfirmpassword"]').val()
      		}, function(data) {
      			//alert(data)
        		if("email" in data) {
        			$("#sh1").text(data.email)
        		}
        		if("username" in data) {
        			$("#sh2").text(data.username)
        		}
        		if("comfirmpassword" in data) {
        			$("#sh4").text(data.comfirmpassword)
        		}
        		if("warn" in data) {
        			alert(data.warn)
        			//$("#sh5").text(data.warn)
        		}
        		$('input[name="email"]').focus().select();
      		});
    	}
      	return false;
    };

    $('#submitBut').bind('click', submit_form);

    $('input[name="email"]').bind("click", function() {
    	$('input[name="email"]').val("")
    	$("#sh1").text("")
    })
    $('input[name="username"]').bind("click", function() {
    	$('input[name="username"]').val("")
    	$("#sh2").text("")
    })
    $('input[name="password"]').bind("click", function() {
    	$('input[name="password"]').val("")
    	$("#sh3").text("")
    })   
    $('input[name="comfirmpassword"]').bind("click", function() {
    	$('input[name="comfirmpassword"]').val("")
    	$("#sh4").text("")
    })
});