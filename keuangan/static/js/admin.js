
async function get_json_cashout() {
    return fetch("/keuangan/json/admin-cashouts/").then((res) => res.json())
}

async function get_json_uang_user() {
    return fetch("/keuangan/json/admin/").then((res) => res.json())
}

// TODO: fix user's username value
// TODO: add POST -> update approve/disburse && uang_user
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
        console.log("No data")
    } else {
        console.log("Success")
        htmlString += `
        <thead>
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Nama</th>
                <th scope="col">Jumlah</th>
                <th scope="col">Approval</th>
                <th scope="col"></th>
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
                <td>${item.fields.approved}</td>
                <td>
                <button class="btn btn-primary text-wrap" onClick="edit_cashout(${item.pk})"> Edit </button>
                </td>
            </tr>
            ` 
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
          
    })

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
    form.addEventListener('submit', function(e) {
        e.preventDefault()

        fetch(`/keuangan/edit-uang-user/${id}/`, {
            method: "POST",
            body: new FormData(document.querySelector('#form-update-uang-user'))
        }).then(document.getElementById("close2").click())
          .then(refresh_table_uang_user)
          
    })

    return false
}

document.getElementById("cashout").onclick = refresh_table_cashout
document.getElementById("uang_user").onclick = refresh_table_uang_user
refresh_table_cashout()