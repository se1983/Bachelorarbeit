var mapLayer = new ol.layer.Tile({
    source: new ol.source.OSM()
});

var image = new ol.style.Circle({
    radius: 2.5,
    fill: null,
    stroke: new ol.style.Stroke({color: 'red', width: 1})
});

var styles = {
    'Point': new ol.style.Style({
        image: image
    })
};

var styleFunction = function (feature) {
    return styles[feature.getGeometry().getType()];
};

var argoFloatsLayer = new ol.layer.Vector({
    style: styleFunction,
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: "/last_seen"
    })
});


var map = new ol.Map({
    layers: [mapLayer, argoFloatsLayer],
    target: 'map',
    controls: ol.control.defaults({
        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
            collapsible: false
        })
    }),
    view: new ol.View({
        center: [0, 0],
        zoom: 2
    })
});


