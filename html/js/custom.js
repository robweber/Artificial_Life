//update on the ui if the program is running
function updateProgramStatus(macro,args,response){
  json = jQuery.parseJSON(response)

  if(json['is_running']){
    
    $('#is_running').html('Running');
    $('#is_running').removeClass('text-danger');
    $('#is_running').addClass('text-success');
  }
  else
  {
    $('#is_running').html('Not Running');
    $('#is_running').removeClass('text-success');
    $('#is_running').addClass('text-danger');

  }
}

//show notifications from webiopi calls
function showNotification(macro,args,response){
  json = jQuery.parseJSON(response)
  $('#alert_area').html(json.message);
  $('#alert_area').fadeIn(300).delay(1500).fadeOut(400);
}

//convert rgb values to hex
var rgbToHex = function (rgb) { 
  var hex = Number(rgb).toString(16);
  if (hex.length < 2) {
       hex = "0" + hex;
  }
  return hex;
};
