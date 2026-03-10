/*
    * Frontend JavaScript code to interact with the backend API and display the list of tables.
*/

const API_URL = "http://127.0.0.1:8000"

async function loadTableData() {

    const params = new URLSearchParams(window.location.search)

    const table = params.get("table")

    if (!table) return

    const response = await fetch(`${API_URL}/data/${table}`)

    const data = await response.json()

    const tableElement = document.getElementById("data-table")

    if (data.length === 0) return

    const headers = Object.keys(data[0])

    const headerRow = document.createElement("tr")

    headers.forEach(h => {

        const th = document.createElement("th")

        th.innerText = h

        headerRow.appendChild(th)

    })

    tableElement.appendChild(headerRow)

    data.forEach(row => {

        const tr = document.createElement("tr")

        headers.forEach(h => {

            const td = document.createElement("td")

            td.innerText = row[h]

            tr.appendChild(td)

        })

        tableElement.appendChild(tr)

    })

}

loadTableData()