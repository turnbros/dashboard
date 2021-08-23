function get_resources() {
    let module_resources = httpAPIGet("resource")
    let resource_table = document.getElementById("module_resource_table");
    resource_table.innerText = ""
    module_resources["resources"].forEach(function(element) {
        if(element["status"] !== "Purged"){
            resource_table.appendChild(create_resource_table_row(element))
        }
    })
}

function get_module_resources() {
    let module_resources = httpAPIGet("resource?module="+workspace_module_name)
    let resource_table = document.getElementById("module_resource_table");
    resource_table.innerText = ""
    module_resources["resources"].forEach(function(element) {
        if(element["status"] !== "Purged"){
            resource_table.appendChild(create_resource_table_row(element))
        }
    })
}

function create_resource_table_row(resource_item){
    let table_row = document.createElement("tr")
    let table_cell_name = document.createElement("td")
    let table_cell_module = document.createElement("td")
    let table_cell_status = document.createElement("td")

    table_cell_name.innerText = resource_item["name"]
    table_cell_module.innerText = resource_item["module"]
    table_cell_status.innerText = resource_item["status"]

    table_row.appendChild(table_cell_name)
    table_row.appendChild(table_cell_module)
    table_row.appendChild(table_cell_status)

    return table_row
}
