const API_URL = "http://127.0.0.1:8000";


/* =========================
   CREATE SCHEMA API CALL
========================= */

async function createSchemaAPI(schema) {

    try {
        const response = await fetch(`${API_URL}/schemas`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(schema)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to create schema");
        }

        return response.json();
    } catch (error) {
        if (error instanceof TypeError && error.message === "Failed to fetch") {
            throw new Error(`Cannot connect to API server at ${API_URL}. Make sure the backend is running.`);
        }
        throw error;
    }
}


/* =========================
   GET SCHEMAS API CALL
========================= */

async function getSchemasAPI() {

    try {
        const response = await fetch(`${API_URL}/schemas`, {
            method: "GET"
        });

        if (!response.ok) {
            throw new Error("Failed to fetch schemas");
        }

        return response.json();
    } catch (error) {
        if (error instanceof TypeError && error.message === "Failed to fetch") {
            throw new Error(`Cannot connect to API server at ${API_URL}. Make sure the backend is running on port 8000.`);
        }
        throw error;
    }
}


/* =========================
   VALIDATE CSV
========================= */

async function validateCSV(table, file) {

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_URL}/validation/${table}`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to validate CSV");
        }

        return response.json();
    } catch (error) {
        if (error instanceof TypeError && error.message === "Failed to fetch") {
            throw new Error(`Cannot connect to API server at ${API_URL}. Make sure the backend is running.`);
        }
        throw error;
    }
}


/* =========================
   INSERT DATA
========================= */

async function insertData(table, data) {

    try {
        const response = await fetch(`${API_URL}/data/${table}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to insert data");
        }

        return response.json();
    } catch (error) {
        if (error instanceof TypeError && error.message === "Failed to fetch") {
            throw new Error(`Cannot connect to API server at ${API_URL}. Make sure the backend is running.`);
        }
        throw error;
    }
}


/* =========================
   UI FUNCTIONS
========================= */

function addColumn() {

    const container = document.getElementById("columns")
    const div = document.createElement("div")

    div.innerHTML = `
        <input placeholder="column name" class="col_name"/>
        
        <select class="col_type">
            <option>string</option>
            <option>integer</option>
            <option>float</option>
            <option>bool</option>
        </select>

        required <input type="checkbox" class="col_required"/>
        unique <input type="checkbox" class="col_unique"/>
    `

    container.appendChild(div)
}


async function createSchema() {

    try {
        const tableName = document.getElementById("table_name").value

        if (!tableName.trim()) {
            alert("Table name is required");
            return;
        }

        const names = document.querySelectorAll(".col_name")
        const types = document.querySelectorAll(".col_type")
        const required = document.querySelectorAll(".col_required")
        const uniques = document.querySelectorAll(".col_unique")

        const columns = []

        for (let i = 0; i < names.length; i++) {
            if (!names[i].value.trim()) {
                alert("All column names are required");
                return;
            }

            columns.push({
                name: names[i].value,
                datatype: types[i].value,
                required: required[i].checked,
                unique: uniques[i].checked
            })
        }

        const payload = {
            table_name: tableName,
            columns: columns
        }

        const result = await createSchemaAPI(payload)

        alert("Schema created successfully!");

        // Refresh schema list
        const schemas = await getSchemasAPI();
        console.log("Stored schemas:", schemas);

    } catch (error) {
        alert("Error creating schema: " + error.message);
        console.error("Error:", error);
    }
}