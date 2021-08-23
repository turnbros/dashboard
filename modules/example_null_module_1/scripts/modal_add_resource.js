

function showModal() {
    var modal = document.getElementById("myModal");
    console.log("open modal")
    let modal_form = document.getElementById("modal_form");
    modal_form.innerHTML = "";
    let modal_header = document.createElement("p")
    modal_header.innerText = "New " + workspace_manifest[workspace_module_name]['title']
    modal_form.appendChild(modal_header);

    let name_input_row = document.createElement("div")
    let name_input_title_column = document.createElement("div")
    let name_input_value_column = document.createElement("div")
    let name_input_title = document.createElement("label");
    let name_input_value = document.createElement("input");

    name_input_row.className = "w3-row w3-padding-small"
    name_input_title_column.className = "w3-col w3-quarter w3-padding-small"
    name_input_value_column.className = "w3-col w3-threequarter w3-padding-small"
    name_input_title.innerText = "Resource Name: ";
    name_input_value.id = "resource_name";

    name_input_title_column.appendChild(name_input_title)
    name_input_value_column.appendChild(name_input_value)
    name_input_row.appendChild(name_input_title_column)
    name_input_row.appendChild(name_input_value_column)
    modal_form.appendChild(name_input_row);

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

        input_title_column.appendChild(input_title)
        input_value_column.appendChild(input_value)
        input_row.appendChild(input_title_column)
        input_row.appendChild(input_value_column)
        modal_form.appendChild(input_row);
    });

    modal.style.display = "block";
}

function submit_modal() {
    console.log("submit modal for new resource")
    let resource_name = document.getElementById("resource_name").value;
    console.log(document.getElementById("resource_name"))
    let resource_parameters = {}
    Object.keys(workspace_manifest[workspace_module_name]['variables']).forEach(function(key) {
        let input_field = document.getElementById(key);
        console.log(input_field)
        resource_parameters[key] = input_field.value;
    });

    let resource_json = {
        "name": resource_name,
        "module": "example_null_module_1",
        "parameters": resource_parameters
    }

    let url = "http://192.168.1.206:8444/tenant/test-tenant-1/resource";
    let xhr = new XMLHttpRequest();
    xhr.open("PUT", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*")
    xhr.onreadystatechange = function () {
       if (xhr.readyState === 4) {
          console.log(xhr.status);
          console.log(xhr.responseText);
       }};

    let myJSON = JSON.stringify(resource_json);
    console.log(myJSON)
    xhr.send(myJSON);
    closeModal()
}

function closeModal() {
    let modal = document.getElementById("myModal");
    console.log("close modal")
    modal.style.display = "none";
    get_module_resources()
}
