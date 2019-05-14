//update on the ui if the program is running
function updateProgramStatus(isRunning){
  if(isRunning){
    
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