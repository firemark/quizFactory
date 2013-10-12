var AnsTypeView = Backbone.View.extend({
    initialize: function(args){
        _.bindAll(this, 'render');
        this.template_begin = _.template(args.template_begin);
        this.template_finish = _.template(args.template_finish);
        this.generate_choice = args.generate_choice;
    },
    render: function(answers, choice, end){
        var template = end?this.template_finish:this.template_begin;
        var str = '<ul class="list-group">';
        _.each(answers, function(obj, hash, list){
            str += template({
                text: obj.text,
                is_correct: obj.is_correct,
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
        template_begin: "<li class='list-group-item <%-choice==hash?'active':''%>'>\
        <input type='radio' name='ans' <%-choice==hash?'checked':''%> value='<%=hash%>' /> <%-text%>\
        </li>",
        template_finish: "<li class='list-group-item'>\
        <input type='radio' name='ans' disabled='disabled' <%-choice==hash?'checked':''%> value='<%=hash%>' /> <%-text%>\
        <% if(is_correct){ %>\
            <span class='label label-default label-success'>OK</span>\
        <% }else if(choice==hash){ %>\
             <span class='label label-default label-danger'>WRONG</span>\
        <% } %>\
        </li>",
        generate_choice: function(form){
            return form.find("input:checked").attr('value');         
        }
    }),
    checkbox: new AnsTypeView({
        template_begin: "<li class='list-group-item <%-choice.indexOf(hash)>=0?'active':''%>'>\
        <input type='checkbox' <%-choice.indexOf(hash)>=0?'checked':''%> name='ans' value='<%=hash%>' /> <%-text%>\
        </li>",
        template_finish: "<li class='list-group-item'>\
        <input type='checkbox' disabled='disabled' <%-choice.indexOf(hash)>=0?'checked':''%> value='<%=hash%>' /> <%-text%>\
        <% if(is_correct){ %>\
            <span class='label label-default label-success'>OK</span>\
        <% }else if(choice.indexOf(hash)>=0){ %>\
             <span class='label label-default label-danger'>WRONG</span>\
        <% } %>\
        </li>",
        generate_choice: function(form){
            var choice = [];
            form.find("input:checked").each(function(index, el){
                choice.push(el.value);
            })

            return choice;
        }
    })
};