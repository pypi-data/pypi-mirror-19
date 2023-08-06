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
        "is_update": false,
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
        action_detail: function() {},
        getDetail: function(name, action, resource) {
            this.model = resource.model;
            this.action = resource.action;

            this.detail.name = name;
            this.detail.action = action;

            var primary_key = actionMap[action]["primary_key"];
            if (primary_key)
                this.detail.link = "/" + name + "/" + "{" + primary_key + "}/";
            else
                this.detail.link = "/" + name + "/";

            if (action == 'update') {
                this.detail.method = 'PATCH'
                this.is_update = true;
                this.detail.args = '';
                this.detail.returns = '';
                this.detail.sends = '';
                var field = resource.action[action]["send"][0]
                var type = this.model[field].type
                if (type == 'bool')
                    this.detail.sends = ['true', 'false']

                var choice = this.model[field].choice
                if (choice)
                    this.detail.sends = choice

                return;
            } else {
                this.is_update = false;
            }

            this.detail.args = resource.action[action]["args"];
            this.detail.returns = resource.action[action]["return"];
            this.detail.sends = resource.action[action]["send"];


            this.detail.method = actionMap[action]["method"];
        },
        updateDetail: function(field) {
            if (this.model) {
                var type = this.model[field].type
                if (type == 'bool')
                    this.detail.sends = ['true', 'false']

                var choice = this.model[field].choice
                if (choice)
                    this.detail.sends = choice
            }
        },
        updateDescription: function(field) {
            if (this.model)
                return "更新" + this.model[field].verbose;
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