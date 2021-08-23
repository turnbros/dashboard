function show_view_resource_modal(resource_name){
    let resource_data = httpAPIGet("resource?name="+resource_name)
    let resource = resource_data["resources"][0]
    let modal = document.getElementById("view_resource_modal");
    let resource_view_title = document.getElementById("view_resource_name");

    resource_view_title.innerText = resource["name"] + " - " + resource["id"]
    build_modal_body("resource_modal_form", resource["parameters"])
    document.getElementById("delete_resource").onclick = delete_resource.bind(this, [resource["id"]])
    modal.style.display = "block";
}

function build_modal_body(modal_form_name, resource_params){
    let modal = document.getElementById(modal_form_name);
    modal.innerHTML = "";
    
    Object.keys(workspace_manifest[workspace_module_name]['variables']).forEach(function(key) {
        let input_row = document.createElement("div")
        let input_title_column = document.createElement("div")
        let input_value_column = document.createElement("div")
        let input_title = document.createElement("label")
        let input_value = document.createElement("input")

        input_row.className = "w3-row w3-padding-small"
        input_title_column.className = "w3-col w3-quarter w3-padding-small"
        input_value_column.className = "w3-col w3-threequarter w3-padding-small"
        input_title.innerText = workspace_manifest[workspace_module_name]['variables'][key]["name"] + ": "
        input_value.id = key
        input_value.value = resource_params[key]

        input_title_column.appendChild(input_title)
        input_value_column.appendChild(input_value)
        input_row.appendChild(input_title_column)
        input_row.appendChild(input_value_column)
        modal.appendChild(input_row);
    });
}

function delete_resource(resource_id){
    httpAPIDelete("resource/" + resource_id)
    close_view_resource_modal()
}

function close_view_resource_modal(){
    let modal = document.getElementById("view_resource_modal");
    modal.style.display = "none";
    get_module_resources()
}