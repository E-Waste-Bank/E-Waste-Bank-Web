// Add Task
function redir() {
    console.log("redir");
    window.location.replace("/tips-and-tricks");
}

$(document).ready(function() {
    $("#detailAdd").submit(function(e) {
        e.preventDefault(); 

        $.ajax({
            url: "/tips-and-tricks/add",
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                console.log("ajax?");
                redir();
            }
        });
    });
});