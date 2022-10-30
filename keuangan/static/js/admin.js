
async function get_json_cashout() {
    return fetch('/keuangan/json/admin_cashout').then((res) => res.json())
}

// 
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
                <th scope="col">Handle</th>
            </tr>
        </thead>

        <tbody>
        `

        data.forEach((item) => {
            htmlString += `
            <tr>
                <th scope="row">${item.pk}</th>
                <td>${item.fields.user}</td>
                <td>${item.fields.user}</td>
                <td>${item.fields.user}</td>
            </tr>
            ` 
        })

        htmlString += `</tbody>`
    }
    document.getElementById("table").innerHTML = htmlString
}

document.getElementById("cashout").onclick = refresh_table_cashout
refresh_table_cashout()