function get_latest_three(){
    cards = ""
    $.getJSON("/about-us/get-latest-three", function (data) {
        $.each(data, function(i, entry) {
            cards+=`
            <div class="card" >
                <div class="card-body" style="background-color:#F8F7F3">
                    <blockquote class="blockquote mb-0">
                        <p>${entry.fields.your_feedback}</p>
                    <footer class="blockquote-footer" style="background-color:#F8F7F3">${entry.fields.name} on ${entry.fields.date}</footer>
                    </blockquote>
                </div>
            </div>
            `
        })
        $("#latest-three-feedback").html(cards)
    })
}



$(document).ready(function(){
    get_latest_three()
    $("#form_add").submit(function (e) {
        e.preventDefault();

        $.ajax({
            url: e.currentTarget.action,
            type: "POST",
            data: $(this).serialize(),
            success: function (data) {
                $("#exampleModal").modal("toggle");
                get_latest_three()
            }, 
            error: function (jqxhr, status, error) {
            },       
        })
        document.getElementById("form_add").reset()
    })
})

