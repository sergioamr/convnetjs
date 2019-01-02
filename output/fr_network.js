layer_defs = []; 
layer_defs.push({type:'input', out_sx:64, out_sy:64, out_depth:3}); 
layer_defs.push({type:'conv', sx:5, filters:32, stride:1, pad:2, activation:'relu'}); 
layer_defs.push({type:'pool', sx:2, stride:2}); 
layer_defs.push({type:'conv', sx:5, filters:40, stride:1, pad:2, activation:'relu'}); 
layer_defs.push({type:'pool', sx:2, stride:2}); 
layer_defs.push({type:'conv', sx:5, filters:40, stride:1, pad:2, activation:'relu'}); 
layer_defs.push({type:'pool', sx:2, stride:2}); 
layer_defs.push({type:'softmax', num_classes: 5 }); 
 
net = new convnetjs.Net(); 
net.makeLayers(layer_defs); 
 
trainer = new convnetjs.SGDTrainer(net, {method:'adadelta', batch_size:31, l2_decay:0.0001}); 
