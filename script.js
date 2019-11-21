
var r=0;
var c=0;
var R=[[-1, -1, -1, -1, 0, -1], 
       [-1, -1, -1, 0, -1, 100],
       [-1, -1, -1, 0, -1, -1],
       [-1, 0, 0, -1, 0, -1],
       [-1, 0, 0, -1, -1, 100],
       [-1, 0, -1, -1, 0, 100]];
var Q_mat=[[0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0]];
 var nodes = new vis.DataSet([
    {id: 0, label: 'Node 0'},
    {id: 1, label: 'Node 1'},
    {id: 2, label: 'Node 2'},
    {id: 3, label: 'Node 3'},
    {id: 4, label: 'Node 4'},
    {id: 5, label: 'Node 5'}
  ]);

  // create an array with edges
  var edges = new vis.DataSet([
    {from: 0, to: 4},
    {from: 1, to: 3},
    {from: 1, to: 5},
    {from: 2, to: 3},
    {from: 3, to: 4},
    {from: 4, to: 5},
    {from: 5, to: 5}

  ]);

var restart = document.querySelector("#b1");
var start=document.querySelector("#b2");
var show_path=document.querySelector("#b3");

var tab1=document.getElementById("tab1") ;
var tab2=document.getElementById("tab2") ;





function change_Q(data,i) { 
 
  setTimeout(function() { 
    for(j in data.Q_Learn[i]){
      var val=data.Q_Learn[i][j];
      var index_rc=j.split('');
      tab2.rows[r].cells[c].style.backgroundColor= "#e6fff1";
      r=Number(index_rc[0]);
      c=Number(index_rc[1]);
    
      tab2.rows[r].cells[c].textContent=Math.round(val);
      tab2.rows[r].cells[c].style.backgroundColor= "#ff4d4d";
    }
  }, 500 * i); 
  
} 

function training_Q(){

  fetch('./model_history.json').then(response => {
      return response.json();
    }).then(data => {
      //JSON data here..
     var states_IF = document.getElementById("train_summary");
   
     states_IF.textContent=data.Training_Summary
      for (k in data.Q_Learn){
        change_Q(data,k);
        
      }
      
    }).catch(err => {
      // when the request fails
      console.log('The request failed!'); 
      
    });
}
function color_path(n){
  var pathNode = nodes.get(n);
  pathNode.color = {
      border: '#ff4d4d',
      background: '#ff4d4d',
      highlight: {
        border: '#ff4d4d',
        background: '#ff4d4d'
      }
    }
   nodes.update(pathNode);
}
function path_nodes(){
   fetch('./model_history.json').then(response => {
   return response.json();
   }).then(data => {
  //JSON data here..
  
   var states_IF = document.getElementById("path_summary");
   
  states_IF.textContent=data.Path_Summary
   for(var i=0; i<data.Path.length;i++){
      color_path(data.Path[i]);
   }
  
  }).catch(err => {
  // when the request fails
   console.log('The request failed!'); 
  
  });
}

start.addEventListener('click',training_Q);
show_path.addEventListener('click',path_nodes)

for (var i = 0 ; i < tab1.rows.length; i++) {
    for (var j = 1; j < tab1.rows[i].cells.length; j++) {

    tab1.rows[i].cells[j].textContent=R[i][j-1];
    }
}
for (var i = 0 ; i < tab2.rows.length; i++) {
    for (var j = 1; j < tab2.rows[i].cells.length; j++) {

    tab2.rows[i].cells[j].textContent=Q_mat[i][j-1];
    }
}


  // create a network
  var container = document.getElementById('mynetwork');
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {autoResize: true};
  var network = new vis.Network(container, data, options);

