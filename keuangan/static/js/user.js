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
    // filter buat ngecek ada elemen yg approved/pending di array ga (pake Array.some())
    const approved = (entry) => entry.fields.approved;
    const pending = (entry) => !(entry.fields.approved);

    $.ajax({
        type: "GET",
        url: "/keuangan/json/user-cashouts/",
        dataType: "json",
        success: function (data) {
            console.log("all cashouts GET success");
            $(".table-cashout-parent").empty();

            // kalau blm ada cashout data akan empty
            if ($.isEmptyObject(data)) {
                $(".table-cashout-parent").append(
                    $(`<h4 class="text-center">`).append(
                        `Belum ada request penarikan!`
                    ).append(
                        `<h5 class="text-center text-muted fst-italic">Yuk, <a href="#" onclick="$('#modal-create-cashout').modal('toggle')">buat penarikan baru</a>!</h5>`
                    )
                );

            } else {
                // Cek jika ada data yg sdh diapprove pake filter yg sdh dibuat
                if (data.some(approved)) {
                    $("#table-done-parent").append(
                        $(`<table class="table table-striped table-hover table-bordered table-sm table-responsive-md mx-auto">`).append(
                            $("<thead>").append(
                                $("<tr>").append(
                                    $(`<th scope="col">`).append(
                                        `ID Penarikan`
                                    )
                                ).append(
                                    $(`<th scope="col">`).append(
                                        `Jumlah Dana yang Ditarik`
                                    )
                                ).append(
                                    $(`<th scope="col">`).append(
                                        `Lihat Detail`
                                    )
                                )
                            )
                        ).append(
                            $(`<tbody class="table-group-divider" id="cashouts-parent">`)
                        )
                    )
                } else {
                    // Jika blm ada samsek data yg sdh diapprove
                    $("#table-done-parent").append(
                        $(`<h4 class="text-center">`).append(
                            `Tidak ada request penarikan yang sudah disetujui!`
                        )
                    );
                }
                
                // Cek jika ada data yg pending pake filter yg sdh dibuat
                if (data.some(pending)) {
                    $("#table-pending-parent").append(
                        $(`<table class="table table-striped table-hover table-bordered table-sm table-responsive-md mx-auto">`).append(
                            $("<thead>").append(
                                $("<tr>").append(
                                    $(`<th scope="col">`).append(
                                        `ID Penarikan`
                                    )
                                ).append(
                                    $(`<th scope="col">`).append(
                                        `Jumlah Dana yang Ditarik`
                                    )
                                ).append(
                                    $(`<th scope="col">`).append(
                                        `Lihat Detail`
                                    )
                                )
                            )
                        ).append(
                            $(`<tbody class="table-group-divider" id="cashouts-parent">`)
                        )
                    )
                } else {
                    // Jika blm ada samsek data yg pending
                    $("#table-pending-parent").append(
                        $(`<h4 class="text-center">`).append(
                            `Tidak ada request penarikan yang belum disetujui!`
                        )
                    );
                }

                $(data).each(function (i, entry) {
                    if (entry.fields.approved) {
                        $("#table-done-parent > .table").append(
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
                    } else {
                        $("#table-pending-parent > .table").append(
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
                    }
                })
            
                if (data.some(approved)) {
                    $("#table-done-parent > .table").DataTable({
                        "searching": false,
                        columnDefs: [
                            {targets: [1,2], orderable: false}
                        ],
                    });
                }

                if (data.some(pending)) {
                    $("#table-pending-parent > .table").DataTable({
                        "searching": false,
                        columnDefs: [
                            {targets: [1,2], orderable: false}
                        ],
                    });
                }
            
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