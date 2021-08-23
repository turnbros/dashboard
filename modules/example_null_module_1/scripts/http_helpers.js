function httpAPIGet(path)
{
    let url = api_base_url + path;
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false ); // false for synchronous request
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
}

function httpAPIPut(path)
{
    let url = api_base_url + path;
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "PUT", url, false ); // false for synchronous request
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
}

function httpAPIPost(path)
{
    let url = api_base_url + path;
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, false ); // false for synchronous request
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
}

function httpAPIDelete(path)
{
    let url = api_base_url + path;
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "DELETE", url, false ); // false for synchronous request
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
}