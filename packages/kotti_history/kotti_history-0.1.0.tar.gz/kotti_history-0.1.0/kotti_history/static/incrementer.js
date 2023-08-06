$(document).ready(function(){
    setTimeout(function(){
        $.post("./history", function(data){
            console.log(data.message);
        });
    }, kotti_history.timeout);
});
