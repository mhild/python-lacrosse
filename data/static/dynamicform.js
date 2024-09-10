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
            payload[known_keys[i]] = document.getElementById('in_text_'+known_keys[i]).value;
        } else {
            console.log('--> readonly');
        }
    }

    console.log(payload);
}