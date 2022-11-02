
async function get_json_cashout() {
    return fetch("/keuangan/json/admin-cashouts/").then((res) => res.json())
}

async function get_json_uang_user() {
    return fetch("/keuangan/json/admin/").then((res) => res.json())
}

// TODO: fix user's username value
async function refresh_table_cashout() {
    document.getElementById("table").innerHTML = ""
    const data = await get_json_cashout()
    let htmlString = ``

    if ($.isEmptyObject(data)) {
        htmlString += `
        <tr>
            <td>Tidak ada request penarikan</td>
        </tr>
        `
    } else {
        htmlString += `
        <thead>
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Nama</th>
                <th scope="col">Jumlah</th>
                <th scope="col">Edit Approval</th>
            </tr>
        </thead>

        <tbody>
        `

        data.forEach((item) => {
            htmlString += `
            <tr>
                <th scope="row">${item.pk}</th>
                <td>${item.fields.user}</td>
                <td>${item.fields.amount}</td>
            ` 

            if (item.fields.approved) {
                htmlString += `
                <td>
                <button class="btn btn-primary text-wrap" onClick="edit_cashout(${item.pk})" style="width: 6rem;"> Selesai </button>
                </td>
                </tr>
                `
            } else {
                htmlString += `
                <td>
                <button class="btn btn-danger text-wrap" onClick="edit_cashout(${item.pk})" style="width: 6rem;"> Pending </button>
                </td>
                </tr>
                `
            }

            // TODO: handle disbursal status
        })

        htmlString += `</tbody>`
    }
    document.getElementById("table").innerHTML = htmlString
}

function edit_cashout(id) {
    $("#modal-update-cashout").modal("toggle")

    var form = document.getElementById('form-update-cashout')
    form.addEventListener('submit', function(e) {
        e.preventDefault()

        fetch(`/keuangan/edit-cashout/${id}/`, {
            method: "POST",
            body: new FormData(document.querySelector('#form-update-cashout'))
        }).then(document.getElementById("close1").click())
          .then(refresh_table_cashout)

          form.reset()
    }, {once : true})

    return false
}

async function refresh_table_uang_user() {
    document.getElementById("table").innerHTML = ""
    const data = await get_json_uang_user()
    let htmlString = ``

    if ($.isEmptyObject(data)) {
        htmlString += `
        <tr>
            <td>Tidak ada data keuangan user</td>
        </tr>
        `
    } else {
        htmlString += `
        <thead>
            <tr>
                <th scope="col">Nama</th>
                <th scope="col">Jumlah</th>
                <th scope="col">Tambah Uang</th>
            </tr>
        </thead>

        <tbody>
        `

        data.forEach((item) => {
            htmlString += `
            <tr>
                <th scope="row">${item.fields.user}</th>
                <td>${item.fields.uang_user}</td>
                <td>
                <button class="btn btn-primary text-wrap" onClick="edit_uang_user(${item.pk})"> Tambah </button>
                </td>
            </tr>
            ` 
        })

        htmlString += `</tbody>`
    }
    document.getElementById("table").innerHTML = htmlString
}

function edit_uang_user(id) {
    $("#modal-update-uang-user").modal("toggle")

    var form = document.getElementById('form-update-uang-user')

    console.log("POST sent")

    form.addEventListener('submit', function(e) {
        e.preventDefault()

        fetch(`/keuangan/edit-uang-user/${id}/`, {
            method: "POST",
            body: new FormData(document.querySelector('#form-update-uang-user'))
        }).then(document.getElementById("close2").click())
          .then(refresh_table_uang_user)

          form.reset()

    }, {once : true})

    return false
}

refresh_table_cashout()

document.getElementById("cashout").onclick = function() {
    refresh_table_cashout()
    document.getElementById("cashout").classList.add("active");
    document.getElementById("uang_user").classList.remove("active");
};

document.getElementById("uang_user").onclick = function() { 
    refresh_table_uang_user()
    document.getElementById("uang_user").classList.add("active");
    document.getElementById("cashout").classList.remove("active");
};