const nativeObject = [];


YAML.load('../../docs/Todo.yml', function(result) {
    nativeObject[0] = result;
    console.log(nativeObject[0]);
});

var docs = new Vue({
    el: '#docs',
    data: {
        doc_array: nativeObject
    }
})