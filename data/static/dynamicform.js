function make_editable(key) {
    document.getElementById('in_text_'+key).readOnly = false;
    document.getElementById('button_'+key).remove();
}

var known_keys = [];
function clear_keys() {
    known_keys = [];
}

function register_key(key) {
    if (!(key in known_keys)) {
        known_keys.push(key);
    } 
}

function submit_mappings() {
    var payload = {};
    for(var i=0; i < known_keys.length; i++) {
        console.log(known_keys[i]);
        if(document.getElementById('in_text_'+known_keys[i]).readOnly == false) {
            payload['id'] = known_keys[i];
            payload['name'] = document.getElementById('in_text_'+known_keys[i]).value;
        } else {
            console.log('--> readonly');
        }
    }

    console.log(payload);

    return fetch('/api/v1/sensors', {
        headers:{
            'Content-Type':'application/json'
            },
        method: 'PUT',
        body: JSON.stringify(payload)
    }).then(response => response.json())
    

}