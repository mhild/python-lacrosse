function make_editable(key) {
    document.getElementById('in_text_'+key).readOnly = false;
    document.getElementById('button_'+key).remove();
}