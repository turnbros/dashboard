function showModal() {
    var modal = document.getElementById("myModal");
    console.log("open modal")

    let modal_form = document.getElementById("modal_form");

    modal_form.innerHTML = "";

    let modal_header = document.createElement("p")
    modal_header.innerText = "New " + workspace_manifest[workspace_module_name]['title']
    modal_form.appendChild(modal_header);

    Object.keys(workspace_manifest[workspace_module_name]['variables']).forEach(function(key) {
        let input_span = document.createElement("span")
        let input_title = document.createElement("p")
        let input_value = document.createElement("input")

        input_title.innerText = workspace_manifest[workspace_module_name]['variables'][key]["name"] + ": "
        input_value.id = key

        input_title.appendChild(input_value);
        input_span.appendChild(input_title);
        modal_form.appendChild(input_span);
    });

    let create_resource_button = document.getElementById("create_resource");
    create_resource_button.onclick = submit_modal()

    modal.style.display = "block";
}

function submit_modal() {
    console.log("submit modal for new resource")
}

function closeModal() {
    var modal = document.getElementById("myModal");
    console.log("close modal")
    modal.style.display = "none";
}
var link = document.querySelector('link[rel="import"]');
link.addEventListener('load', function(e) {
  var importedDoc = link.import;
  console.log(importedDoc)
  // importedDoc points to the document under component.html
});
