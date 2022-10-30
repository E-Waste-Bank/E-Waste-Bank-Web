
async function get_json_cashout() {
    return fetch("keuangan/json/admin-cashout").then((res) => res.json())
}

async function refresh_table() {
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
                <th scope="col">Nama</th>
                <th scope="col">Jumlah</th>
                <th scope="col">Tombol</th>
                <th scope="col">Handle</th>
            </tr>
        </thead>

        <tbody>
        `

        data.forEach((item) => {
            htmlString += `
            <tr>
                <th scope="row">${item.fields.user}</th>
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

document.getElementById("refresh").onclick = refresh_table
refresh_table()