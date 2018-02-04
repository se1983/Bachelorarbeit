// http://plnkr.co/edit/zbqKeJ4lXQ8C60TC4fza?p=preview

var mapLayer = new ol.layer.Tile({
    source: new ol.source.OSM()
});

// TODO Vector layer css kämpft gegen bootstraps style
var mapVectorLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
        url: '/static/countries.geo.json',
        format: new ol.format.GeoJSON()
    })
});

function geometryStyle(feature) {
    var style = [],
        feature_properities = feature.getProperties()['identifier'],
        white = [255, 255, 255, 1],
        blue = [0, 153, 255, 1],
        width = 1;


    var style = [
        new ol.style.Style({
            image: new ol.style.Circle({
                radius: width * 2,
                fill: new ol.style.Fill({color: blue}),
                stroke: new ol.style.Stroke({
                    color: white, width: width / 2
                })
            })
        })
    ];

    return style;
}

function hoverStyle() {
    var
        white = [255, 255, 255, 1],
        blue = [0, 153, 255, 1],
        width = 3;

    var style = [
        new ol.style.Style({
            image: new ol.style.Circle({
                radius: width * 2,
                fill: new ol.style.Fill({color: blue}),
                stroke: new ol.style.Stroke({
                    color: white, width: width / 2
                })
            })
        })
    ];

    return style;
}


var argoFloatsLayer = new ol.layer.Vector({
    style: geometryStyle,
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
        zoom: 3.5,
        minZoom: 3
    })
});

var hoverInteraction = new ol.interaction.Select({
    condition: ol.events.condition.pointerMove,
    layers: [argoFloatsLayer]
});
map.addInteraction(hoverInteraction);

var featureOverlay = new ol.FeatureOverlay({
    map: map,
    style: hoverStyle
});

hoverInteraction.on('select', function (evt) {
    if (evt.selected.length > 0) {
        console.info('selected: ' + evt.selected[0].getId());

    }
});


