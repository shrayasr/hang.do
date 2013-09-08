exports.findAll = function(req, res) {
    res.send([{name:'bars1'}, {name:'bars2'}, {name:'bars3'}]);
};
 
exports.findById = function(req, res) {
    res.send({id:req.params.id, name: "The Name", description: "description"});
};

