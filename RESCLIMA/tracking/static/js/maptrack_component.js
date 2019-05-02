function rainbow(numOfSteps, step) {
    // This function generates vibrant, "evenly spaced" colours (i.e. no clustering). This is ideal for creating easily distinguishable vibrant markers in Google Maps and other apps.
    // Adam Cole, 2011-Sept-14
    // HSV to RBG adapted from: http://mjijackson.com/2008/02/rgb-to-hsl-and-rgb-to-hsv-color-model-conversion-algorithms-in-javascript
    var r, g, b;
    var h = step / numOfSteps;
    var i = ~~(h * 6);
    var f = h * 6 - i;
    var q = 1 - f;
    switch(i % 6){
        case 0: r = 1; g = f; b = 0; break;
        case 1: r = q; g = 1; b = 0; break;
        case 2: r = 0; g = 1; b = f; break;
        case 3: r = 0; g = q; b = 1; break;
        case 4: r = f; g = 0; b = 1; break;
        case 5: r = 1; g = 0; b = q; break;
    }
    var c = "#" + ("00" + (~ ~(r * 255)).toString(16)).slice(-2) + ("00" + (~ ~(g * 255)).toString(16)).slice(-2) + ("00" + (~ ~(b * 255)).toString(16)).slice(-2);
    return (c);
}

/**Funcion que recibe un layer component y datos de longitud
 * y latitud y grafica un punto segun cada lectura y finalmente
 * las grafica el la capa y agrega la capa al mapa
 * el formato de los datos para graficar el viaje es un archivo .gpx
 */
function drawTravel(map, location_file_gpx){
    var colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f']
    color = colors[Math.random() * colors.length | 0]

    var lgpx = new OpenLayers.Layer.Vector("Lakeside cycle ride", {
        strategies: [new OpenLayers.Strategy.Fixed()],
        protocol: new OpenLayers.Protocol.HTTP({
            url: location_file_gpx,
            format: new OpenLayers.Format.GPX()
        }),
        style: {strokeColor: color, strokeWidth: 5, strokeOpacity: 0.5},
        projection: new OpenLayers.Projection("EPSG:4326")
    });

    // se agrega la capa al mapa
    map.addLayer(lgpx);
}



