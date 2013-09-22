YUI().use("node","model","view","model-list",function(Y){
    console.log("You are up!");
    create_suggestion_model(Y);
    create_suggestion_submodel(Y);
    create_suggestion_list(Y);
    create_suggestion_view(Y);
    create_suggestion_view_list(Y);
    var xlist = new Y.suggestion_list();
    xlist.sync("kormangala");
});

function create_suggestion_model(Y) {
    var procs = {
	"parse":function(data) {
	    return new Y.suggestion_submodel(data);
	},
	"add":function(e) {
	    console.log(e);
	}
    };
    var attrs = {
	"movie":{
	    "value":null
	},
	"food":{
	    "value":null
	},
	"approx_budget":{
	    "value":null
	}
    };
    var suggestion_model = Y.suggestion_model = new Y.Base.create("suggestion_model",Y.Model,[],procs,{"ATTRS":attrs});
}

function create_suggestion_submodel(Y) {
    var procs = {};
    var attrs = {
	"name":{
	    "value":null
	},
	"location":{
	    "value":null
	},
	"address":{
	    "value":null
	},
	"cost":{
	    "value":null
	},
	"phone":{
	    "value":null
	},
	"rating":{
	    "value":null
	}
    };
    var suggestion_submodel = Y.suggestion_submodel = new Y.Base.create("suggestion_model",Y.Model,[],procs,{"ATTRS":attrs});
}

function create_suggestion_list(Y) {
    var procs = {
	"model":Y.suggestion_model,
	"sync":function(location) {
	    list = this,
	    load = function(response){
		list.add(response);
		console.log("list synced");
	    };
	    failed = function(xhr) {
		console.log("call failed");
	    };

	    $.ajax({
		"url":"suggestions.json",
		"type":"GET",
		"async":true,
		"success":load,
		"error":failed
	    });
	}
    };
    var suggestion_list = Y.suggestion_list = new Y.Base.create("suggestion_list",Y.ModelList,[],procs);
}

function create_suggestion_view(Y) {
    var procs = {
	"template":Y.one("#suggestion-box-template").getContent(),
	"initializer":function(e) {
	    var model = e.model;
	    this.set("model",model);
	    model.on("change",this.update);
	},
	"render":function() {
	    var container = this.get("container"),
	    model = this.get("model"),
	    content = Y.Lang.sub(this.template,{"suggestion":model.get("plan")});
	    
	},
	"add":function(e) {
	    
	},
	"update":function(e) {

	},
	"reset":function(e) {
	    
	},
	"destroy":function(e) {
	    this.destroy();
	}
    };
    var attrs = {
	"container":{
	    "valueFn":function() {
		
	    },
	    "model":{
		"value":null
	    }
	}
    };
    var s_view = Y.suggestion_view = new Y.Base.create("suggestion_view",Y.View,[],procs,{"ATTRS":attrs});
}

function create_suggestion_view_list(Y) {
    var procs = {
	"initializer":function(e) {
	    var modellist = e.modellist;
	    this.set("modellist",modellist);
	    modellist.on("add",this.add,this);
	    modellist.on("remove",this.remove,this);
	    modellist.on("reset",this.reset,this);
	},
	"render":function() {
	    var modellist = this.get("modellist"),
	    container = this.get("container");
	    var build_view = function(model) {
		var x_view = new Y.suggestion_view({"model":model});
		container.append(x_view.render().get("container"));
	    };
	    modellist.each(build_view);
	},
	"add":function(e) {
	    var container = this.get("container"),
	    x_view = new Y.suggestion_view({"model":e.model});
	    container.append(x_view.render().get("container"));
	},
	"remove":function(e) {

	},
	"reset":function(e) {
	    
	}
    };
    var attrs = {
	"container":{
	    "valueFn":function() {

	    }
	},
	"modellist":{
	    "value":null
	}
    };
    var s_view_list = Y.suggestion_view_list = new Y.Base.create("suggestion_view_list",Y.View,[],procs,{"ATTRS":attrs});
}
