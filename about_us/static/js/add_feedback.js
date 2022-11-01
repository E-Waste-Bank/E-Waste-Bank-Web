function get_latest_three(){
    cards = ""
    $.getJSON("/about-us/get-latest-three", function (data) {
        $.each(data, function(i, entry) {
            cards+=`
            <div class="card-deck" style="max-width:1330px;">
                <div class="card">
                    <div class="card-body">
                        <h4 class="card-title">${entry.fields.name}</h4>
                        <medium class="card-subtitle mb-2 text-muted">${entry.fields.date}</medium>
                        <p class="card-text">${entry.fields.your_feedback}</p>
                    </div>
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
                $(".modal-body > p > input").each(function (i) {
                    $(this).val("");
                });
                get_latest_three()
            }, 
            error: function (jqxhr, status, error) {
            },
        })
    })
})

