$(document).ready(function(c) {
	$('.alert-close').on('click', function(c){
		$('.message').fadeOut('slow', function(c){
	  		$('.message').remove();
		});
	});	  

    var submit_form = function(e) {
      	$.post($SCRIPT_ROOT + '/login', {
        	email: $('input[name="email"]').val(),
        	password: $('input[name="password"]').val(),
      	}, function(data) {
            //alert("data rec")
        	if("email" in data) {
                //alert("lala")
                //alert(data.email)
        		$("#sh1").text(data.email)
        	}
        	if("password" in data) {
        		$("#sh3").text(data.password)
        	}
        	$('input[name="email"]').focus().select();
        	if("success" in data) {
        		$("#sh5").text("Login successfully")
        		window.location.href = "/user?username=" + data.success
        	}
      	});
      	return false;
    };

    $('#submitBut').bind('click', submit_form);

    $('input[name="email"]').bind("click", function() {
        $('input[name="email"]').val("")
        $("#sh1").text("")
    })
    $('input[name="password"]').bind("click", function() {
        $('input[name="password"]').val("")
        $("#sh3").text("")
    })   

  
});