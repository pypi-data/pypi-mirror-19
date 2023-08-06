const actionMap = {
    "create": {
        "method": "POST",
        "description": "创建"
    },
    "destroy": {
        "method": "DELETE",
        "description": "删除",
        "primary_key": "id"
    },
    "list": {
        "method": "GET",
        "description": "列表"
    },
    "replace": {
        "method": "PUT",
        "description": "替换",
        "primary_key": "id"
    },
    "retrieve": {
        "method": "GET",
        "description": "详情",
        "primary_key": "id"
    },
    "update": {
        "method": "PATCH",
        "description": "更新",
        "primary_key": "id"
    }
};
const resources = [];

var docs = new Vue({
    el: '#docs',
    data: {
        "resources": resources,
        "model": "",
        "action": "",
        "detail": {
            "name": "",
            "action": "",
            "method": "",
            "link": "",
            "args": "",
            "returns": "",
            "sends": ""
        }
    },
    computed: {
        detail_args: function() {}
    },
    methods: {
        action_description: function(action, description) {
            return actionMap[action].description + description
        },
        action_detail: function() {

        },
        getDetail: function(name, action, resource) {
            this.model = resource.model;
            this.action = resource.action;

            this.detail.name = name;
            this.detail.action = action;

            this.detail.args = resource.action[action]["args"];
            this.detail.returns = resource.action[action]["return"];
            this.detail.sends = resource.action[action]["send"];

            this.detail.method = actionMap[action]["method"];
            var primary_key = actionMap[action]["primary_key"];
            if (primary_key)
                this.detail.link = "/" + name + "/" + "{" + primary_key + "}/";
            else
                this.detail.link = "/" + name + "/";
        },
        argsDetail: function(arg) {
            var arg_detail = this.model[arg]
            var arg_string = arg
            if (arg_detail) {
                for (var k in arg_detail) {
                    arg_string += (" " + arg_detail[k])
                }
                return arg_string
            } else {
                return arg
            }
        }
    }
})













YAML.load('resource', function(ymls) {
    console.log("ymls:  " + ymls);
    for (item in ymls) {
        var yml_path = 'docs/' + ymls[item];
        YAML.load(yml_path, function(result) {
            resources.push(result);
            console.log("yml" + item + ":  ");
            console.log(resources[item]);
        });
    }
});