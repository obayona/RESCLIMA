$(".con-checks").find("input[type='checkbox']").change(function(){
console.log($(this).val())
})

var bboxSelector;

function renderResults(results){
    var layers = results["layers"];
    var length = layers.length;
    if(length == 0){
        results_container.innerHTML = "<h3>No hay resultados</h3>"
        return;
    }


    results_container.innerHTML = "<h2>Resultados:</h2>";

    for(var i=0; i< length; i++){
        var layer = layers[i];
        var div = document.createElement("div");
        var h3 = document.createElement("h3");
        h3.innerHTML = layer["title"];
        var h5 = document.createElement("h5");
        h5.innerHTML = layer["abstract"];
        var a = document.createElement("a");
        a.innerHTML = "Visualizar"
        a.href = layer["type"]+"/view/"+layer["id"];
        var b = document.createElement("a");
        b.innerHTML = "Descargar"
        b.href = layer["type"]+"/export/"+layer["id"];

        div.appendChild(h3);
        div.appendChild(h5);
        div.appendChild(a);
        div.appendChild(b);
        div.style.borderStyle = "solid";
        div.style.borderWidth = "2px";
        div.style.borderColor = "blue";
        div.style.padding = "5px";

        results_container.appendChild(div);

    }
}

function search(text_query,bbox){
    if(text_query=="" && bbox==null) {
        return;
    }
    else if (text_query=="") {
        var url = "search/layer?q="+"&left="+String(bbox["minX"])+"&right="+String(bbox["maxX"])+"&bottom="+String(bbox["minY"])+"&top="+String(bbox["maxY"]);
        console.log("**** url",url);
        var request = $.get(url);
        request.done(function(results){
            renderResults(results)
        })
    }
    else if (bbox==null) {
        var url = "search/layer?q="+text_query+"&left=0&right=0&bottom=0&top=0";
        console.log("**** url",url);
        var request = $.get(url);
        request.done(function(results){
            renderResults(results)
        })
    }
    else {
        var url = "search/layer?q="+text_query+"&left="+String(bbox["minX"])+"&right="+String(bbox["maxX"])+"&bottom="+String(bbox["minY"])+"&top="+String(bbox["maxY"]);               
        console.log("**** url",url);
        var request = $.get(url);
        request.done(function(results){
            renderResults(results)
        })
    }
}


function init(){
    
    var map_container = document.getElementById("bbox_selector_container");
    bboxSelector = new BboxSelector(map_container);

    search_button.addEventListener("click",function(event){
        var text_query = search_input.value;
        console.log("****query text",text_query);
        var bbox = bboxSelector.getBBox();
        console.log("****El bounding box",bbox);
        search(text_query,bbox);
    });
}


    

window.addEventListener("load",init);
