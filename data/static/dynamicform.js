function make_editable(key) {
    document.getElementById('in_text_'+key).readOnly = false;
    document.getElementById('button_'+key).remove();
}

var known_keys = [];
function clear_keys() {
    known_keys = [];
}

function calc_relative_date(datetimestring) {
    var lastseen = Date.parse(datetimestring);
    var now = Date.now();

    var delta = Math.floor((now - lastseen)/1000);

    if (delta<5) {
        return('just now');
    } 
    else if (delta<60) {
        return((Math.floor(delta/5))*5 + 's ago');    
    } 
    else if(delta<3600) {
        return(Math.floor(delta/60) + 'm ago');
    }  
    else if(delta<(3600*24)) {
        return(Math.floor(delta/(3600)) + 'h ago');
    }
    else if(delta<(3600*24*14)) {
        return(Math.floor(delta/(3600*24)) + 'd ago');
    }            
    return ('gone');
}

function update_lastseen() {
    fetch('/api/v1/sensors')
    .then(response => {
        if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }
        return response.json();
    })
    .then(json => {
        console.log(json);
        /*var result = JSON.parse(json);*/
        //console.log(result);
        let orphaned_ids = known_keys.filter(x => !Object.keys(json).includes(x));
        let new_ids = Object.keys(json).filter(x => !known_keys.includes(x));
        console.log('orphaned ids :' + orphaned_ids);
        console.log('new ids :' + new_ids);

        for (const key in json) {
            document.getElementById("label_"+key).setAttribute('data-badge', calc_relative_date(json[key].lastseen));
        }
    })
    .catch(function () {
        this.dataError = true;
    })
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

