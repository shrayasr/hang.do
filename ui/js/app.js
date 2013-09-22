YUI().use("node","model","view","model-list",function(Y){
    console.log("You are up!");
    create_suggestion_model(Y);
    create_suggestion_submodel(Y);
    create_suggestion_list(Y);
    create_suggestion_view(Y);
    create_suggestion_view_list(Y);
    var callService = function(e) {
	var location = Y.one("#my-loc").get("value");
	if(location.length !== 0 && location !== " ") {
	    search_suggestions(Y,location);
	}
    }
    Y.one("#kaboom").on("click",callService);
    
});

function search_suggestions(Y,location) {
    var xlist = new Y.suggestion_list();
    xlist.sync("kormangala");
    var list_view = new Y.suggestion_view_list({"modellist":xlist,"srcNode":"#suggestions-container"});
    list_view.render();
    list_view.update();
}

function create_suggestion_model(Y) {
    var procs = {
	"parse":function(data) {
	    return new Y.suggestion_submodel(data);
	}
	
    };
    var attrs = {
	"movie":{
	    "value":null
	},
	"food":{
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
	"location_specific":{
	    "value":null
	},
	"location_coarse":{
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
	},
	"time":{
	    "value":null
	}
    };
    var suggestion_submodel = Y.suggestion_submodel = new Y.Base.create("suggestion_model",Y.Model,[],procs,{"ATTRS":attrs});
}

function create_suggestion_list(Y) {
    var procs = {
	"model":Y.suggestion_model,
	"sync":function(location) {
	    var list = this,
	    load = function(response){
		list.add(response.suggestions);
		console.log("list synced");
		//console.log(response);
	    },
	    failed = function(xhr) {
		console.log("call failed");
	    };

	    $.ajax({
		"url":encodeURI("suggestions.json"),
		"type":"GET",
		"dataType":"json",
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
	    subs_json = {
		"m_name":model.get("movie").name,
		"m_location":model.get("movie").name_extra,
		"m_time":model.get("movie").time,
		"r_name":model.get("food").name,
		"r_location":model.get("food").location_coarse,
		"appx_cost":parseInt(model.get("food").cost,10)+parseInt(model.get("movie").cost,10)
		
	    },
	    content = Y.Lang.sub(this.template,subs_json),
	    index = model.get("clientId").substring(model.get("clientId").length-1,model.get("clientId").length);
	    container.one('.accordion-inner').setContent(content);
	    container.one(".loc-image").set("src",this.getMapUrl(model));
	    container.one('.accordion-toggle').setContent("Hangout Idea #"+index);
	    return this;
	},
	"getMapUrl":function(model) {
	    var url = "http://maps.googleapis.com/maps/api/staticmap?",
	    map_center = "center="+model.get("movie").location_coarse,
	    map_size="&size=600x300",
	    map_type="&maptype=roadmap",
	    map_markers = this.getMarkers(model),
	    map_sensor = "&sensor=false";
	    //console.log(url+map_center+map_size+map_type+map_markers+map_sensor);
	    return url+map_center+map_size+map_type+map_markers+map_sensor;
	},
	"getMarkers":function(model) {
	    var attrs = ["movie","food"],
	    marker_string = "";
	    for(a in attrs) {
		var loc = model.get(attrs[a]).location_specific,
		symbol = attrs[a].substring(0,1).toUpperCase();
		marker_string += "&markers=color:red|label:"+symbol+"|"+loc;
	    }
	    return marker_string;
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
		var a_main = Y.Node.create("<div class='accordion-group'/>"),
		a_head = Y.Node.create("<div class='accordion-heading'/>"),
		a_link = Y.Node.create("<a class='accordion-toggle' data-toggle='collapse'/>"),
		a_body = Y.Node.create("<div class='accordion-body '/>"),
		a_inner = Y.Node.create("<div class='accordion-inner'/>");
		a_body.setAttribute("id",a_body.get("_yuid"));
		a_link.setAttribute("href","#"+a_body.getAttribute("id"));
		a_head.appendChild(a_link);
		a_body.appendChild(a_inner);
		a_main.appendChild(a_head);
		a_main.appendChild(a_body);
		return a_main;
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
	    var modellist = e.modellist,
	    srcnode = e.srcNode;
	    this.set("modellist",modellist);
	    this.set("srcNode",srcnode);
	    modellist.on("add",this.add,this);
	    modellist.on("remove",this.remove,this);
	    modellist.on("reset",this.reset,this);
	},
	"render":function() {
	    var modellist = this.get("modellist"),
	    container = this.get("container"),
	    srcnode = this.get("srcNode");
	    Y.one(srcnode).setContent(container);
	    return this;
	},
	"add":function(e) {
	    var container = this.get("container"),
	    x_view = new Y.suggestion_view({"model":e.model});
	    container.append(x_view.render().get("container"));
	},
	"remove":function(e) {
	    
	},
	"reset":function(e) {
	    
	},
	"update":function() {
	    var list = this.get("modellist"),
	    container = this.get("container"),
	    build_view = function(model,index) {
		var x_view = new Y.suggestion_view({"model":model}),
		content = x_view.render().get("container");
		container.append(content);
		container.one(".accordion-toggle").setAttribute("data-parent","#"+container.get("id"));
	    };
	    list.each(build_view);
	}
	
    };
    var attrs = {
	"container":{
	    "valueFn":function() {
		var c = Y.Node.create("<div class='accordion'/>");
		c.set("id",c.get("_yuid"));
		return c;
	    }
	},
	"modellist":{
	    "value":null
	},
	"srcNode":{
	    "value":null
	}
    };
    var s_view_list = Y.suggestion_view_list = new Y.Base.create("suggestion_view_list",Y.View,[],procs,{"ATTRS":attrs});
}
