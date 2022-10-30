
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
                <th scope="col">Status</th>
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
                <td>${item.fields.user}</td>
            </tr>
            ` 
        })

        htmlString += `</tbody>`
    }
    document.getElementById("table").innerHTML = htmlString
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
        console.log("No data")
    } else {
        console.log("Success")
        htmlString += `
        <thead>
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Nama</th>
                <th scope="col">Jumlah</th>
            </tr>
        </thead>

        <tbody>
        `

        data.forEach((item) => {
            htmlString += `
            <tr>
                <th scope="row">${item.pk}</th>
                <td>${item.fields.user}</td>
                <td>${item.fields.uang_user}</td>
            </tr>
            ` 
        })

        htmlString += `</tbody>`
    }
    document.getElementById("table").innerHTML = htmlString
}

document.getElementById("cashout").onclick = refresh_table_cashout
document.getElementById("uang_user").onclick = refresh_table_uang_user
refresh_table_cashout()