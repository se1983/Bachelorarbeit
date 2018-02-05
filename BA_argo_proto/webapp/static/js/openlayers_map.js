// http://plnkr.co/edit/zbqKeJ4lXQ8C60TC4fza?p=preview
// http://jsfiddle.net/expedio/mz19nzug/
var mapLayer = new ol.layer.Tile({
    source: new ol.source.OSM()
});


var defaultStyle =
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: [0, 0, 0, 1]
        }),
        stroke: new ol.style.Stroke({
            color: [0, 0, 0, 1],
            width: 1
        })
    });
// TODO Vector layer css kämpft gegen bootstraps style
var mapVectorLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
        url: '/static/countries.geo.json',
        format: new ol.format.GeoJSON()
    }),
});

function FloatStyle(feature) {
    var style = [],
        feature_properities = feature.getProperties()['identifier'],
        white = [255, 255, 255, 1],
        blue = [0, 153, 255, 1],
        width = 1;

    // TODO different styles for different floatstates
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
    style: FloatStyle,
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: "/last_seen"
    })
});


var map = new ol.Map({
    layers: [mapVectorLayer, argoFloatsLayer],
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

/* Hover Stylechange */
// change the style of a float if the pointer is hovering.
// This will give the user a feedback which float is waiting for interaction.
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

var hoverInteraction = new ol.interaction.Select({
    condition: ol.events.condition.pointerMove,
    layers: [argoFloatsLayer]
});
map.addInteraction(hoverInteraction);

var featureOverlay = new ol.layer.Vector({
    map: map,
    useSpatialIndex: false,
    updateWhileAnimating: true,
    updateWhileInteracting: true,
    style: hoverStyle,
});

hoverInteraction.on('select', function (evt) {
    if (evt.selected.length > 0) {
        console.info('selected: ' + evt.selected[0].getId());

    }
});

////////////////////////////////////////////////7


/* Tooltips */
// A tooltip will be shown if the pointer hovers over a ArgoFloat Feature
var info = $('#info');
info.tooltip({
    animation: false,
    trigger: 'manual',
    html: true
});

var displayFeatureInfo = function (pixel) {

    info.css({
        left: pixel[0] + 'px',
        top: (pixel[1] - 15) + 'px'
    });
    var feature = map.forEachFeatureAtPixel(pixel, function (feature, layer) {
        return feature;
    });
    if (feature && feature.getGeometry().getType() === 'Point') {
        console.log();
        var properties = feature.getProperties(),
            identifier = properties['identifier'],
            last_seen = new Date(Date.parse(properties['last_seen'])).toDateString(),
            tooltip_text = '<strong>' + identifier + '</strong>' + '</br>' + last_seen;

        info.tooltip('hide')
            .attr('data-original-title', tooltip_text)
            .tooltip('fixTitle')
            .tooltip('show');
    } else {
        info.tooltip('hide');
    }
};

map.on('pointermove', function (evt) {
    if (evt.dragging) {
        info.tooltip('hide');
        return;
    }
    displayFeatureInfo(map.getEventPixel(evt.originalEvent));
});

/////////////////