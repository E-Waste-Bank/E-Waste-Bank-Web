function refresh_dana_tersedia() {
    $.getJSON("/keuangan/json/user/", function (data) {
        $.each(data, function(i, entry) {
            $("#id-uang-user").text(`Rp${entry.fields.uang_user.toLocaleString('en', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            })}`)
        })
    })
}

function refresh_cashouts() {
    $.ajax({
        type: "GET",
        url: "/keuangan/json/user-cashouts/",
        dataType: "json",
        success: function (data) {
            console.log("all cashouts GET success");
            $("#table-parent").empty();

            // kalau blm ada cashout data akan empty
            if ($.isEmptyObject(data)) {
                $("#table-parent").append(
                    $(`<h3>`).append(
                        `Belum ada request penarikan!`
                    )
                );

            } else {
                $("#table-parent").append(
                    $(`<table class="table table-striped table-hover table-hover table-bordered mx-auto" id="table-cashouts">`).append(
                        $("<thead>").append(
                            $("<tr>").append(
                                $(`<th scope="col">`).append(
                                    `ID Penarikan`
                                )
                            ).append(
                                $(`<th scope="col">`).append(
                                    `Jumlah`
                                )
                            ).append(
                                $(`<th scope="col">`).append(
                                    `Tombol`
                                )
                            )
                        )
                    ).append(
                        $(`<tbody class="table-group-divider" id="cashouts-parent">`)
                    )
                );
                $(data).each(function (i, entry) {
                    $("#table-cashouts").append(
                                $(`<tr>`).append(
                                    $(`<td scope="col">`).append(
                                        entry.pk
                                    )
                                ).append(
                                    $(`<td scope="col">`).append(
                                        `Rp${entry.fields.amount.toLocaleString('en', {
                                            minimumFractionDigits: 2,
                                            maximumFractionDigits: 2
                                        })}`
                                    )
                                ).append(
                                    $(`<td scope="col">`).append(
                                        $(`<a href="/keuangan/cashout/${entry.pk}/" class="btn btn-primary text-wrap">`).append(
                                            `Lihat Detail`
                                        )
                                    )
                                )
                    )
                    
                })
            }
        },
    })
}

$(document).ready(function() {
    refresh_dana_tersedia();
    refresh_cashouts();
    $("#form-create-cashout").submit(function (e) {
        e.preventDefault();

        $("#div-errors").empty();

        $.ajax({
            url: e.currentTarget.action,
            type: "POST",
            data: $(this).serialize(),
            success: function (data) {
                console.log("create cashout POST success");
                $("#modal-create-cashout").modal("toggle");
                $("#form-create-cashout > p > .form-control").each(function (i) {
                    $(this).val("");
                });
                refresh_dana_tersedia();
                refresh_cashouts();
            }, 
            error: function (jqxhr, status, error) {
                jqxhrObj = JSON.parse(jqxhr.responseText)
                if (jqxhr.status == 400) {
                    console.log("Server sent back 400")
                    $("#div-errors").prepend(
                        $(`<p class="text-danger fw-semibold">`).append(
                            `${jqxhrObj['status']}`
                        )
                    )
                }
            }
        })
    })
})