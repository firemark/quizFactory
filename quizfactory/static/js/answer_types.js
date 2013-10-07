var AnsTypeView = Backbone.View.extend({
    initialize: function(args){
        _.bindAll(this, 'render');
        this.template = _.template(args.template);
    },
    render: function(answers, choice){
        var template = this.template;
        var str = '<ul class="list-group">';
        _.each(answers, function(text, hash, list){
            str += template({
                text: text,
                hash: hash,
                choice: choice
            });
        });
        str += '</ul>';
        return str;
    }
})

var AnsTypeViews = {
    radio: new AnsTypeView({
        template: "<li class='list-group-item'>\
        <input type='radio' name='<%=hash%>' /> <%-text%>\
        </li>"
    }),
    checkbox: new AnsTypeView({
        template: "<li class='list-group-item'>\
        <input type='checkbox' name='<%=hash%>' /> <%-text%>\
        </li>"
    })
};