function resize_container(args){

    var screen_width = window.innerWidth;
    var screen_height = window.innerHeight - 20;
  
    d3.select(args.root)
      .style('width', screen_width+'px')
      .style('height', screen_height+'px');
  }

window.onload = function(){
    let hzome = ini_hzome()
    console.log(document.getElementById("viz_json").innerText);

    let network_data = JSON.parse(document.getElementById("viz_json").innerText);
    let args = {
        'root': '#clustergrammerDisplay',
        'network_data': network_data,
        'row_tip_callback':hzome.gene_info,
    }
    resize_container(args)
    let cgm = Clustergrammer(args);
};

