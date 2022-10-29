// Add Task
$(document).ready(function() {
    $("#submitBtn").on('click', function() {
        $.ajax({
            url: "/tips-and-tricks/add",
            type: 'POST',
            dataType:"json",
            success: function(data) {
                window.location.href = "/tips-and-tricks/";
            }
        });
    });
});