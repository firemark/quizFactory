var AnsTypeView = Backbone.View.extend({
    initialize: function(args){
        _.bindAll(this, 'render');
        this.template_begin = _.template(args.template_begin);
        this.template_finish = _.template(args.template_finish);
        this.generate_choice = args.generate_choice;
        if (args.render)
            this.render = args.render;
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
            return form.find("input:checked").val();         
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
    }),
    text: new AnsTypeView({
        template_begin: "Answer: <input type='text' class='form-control' value='<%-choice%>' />",
        template_finish: "Answer: <input type='text' class='form-control' value='<%-choice%>' disabled />\
        <% if(is_correct){ %>\
            <span class='label label-default label-success'>OK</span>\
        <% }else{ %>\
            <span class='label label-default label-danger'>WRONG</span>\
            Good answers: \
            <% _.each(good_answers,function(ans,key,list){ %>\
                <span class='label label-info'><%-ans%></span>\
            <% }) %>\
        <% } %>",
        generate_choice: function(form){
            return form.find("input[type=\"text\"]").val()
        },
        render: function(answers, choice, end){
            if (!end){
                return this.template_begin({choice: choice})
            }else{
                var is_correct = false;
                var good_answers = [];
                var trim_choice = choice.trim()
                _.each(answers, function(obj, hash, list){
                    if (obj.is_correct){
                        var txt = obj.text.trim();
                        if (trim_choice == txt)
                            is_correct = true;
                        good_answers.push(txt);
                    }  
                })
                return this.template_finish({
                    is_correct: is_correct,
                    good_answers: good_answers,
                    choice: choice
                })
            }
        }
    })
};