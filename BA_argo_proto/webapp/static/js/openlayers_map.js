// http://plnkr.co/edit/zbqKeJ4lXQ8C60TC4fza?p=preview
// http://jsfiddle.net/expedio/mz19nzug/
// https://openlayers.org/en/latest/examples/select-features.html
var mapLayer = new ol.layer.Tile({
    source: new ol.source.OSM()
});

var stamen_layer = new ol.layer.Tile({
    source: new ol.source.Stamen({
        layer: 'watercolor'
    })
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
        red = [255, 0, 0, 1];
    blue = [0, 153, 255, 1],
        width = 1;

    // TODO different styles for different floatstates
    style['latest_position'] = [
        new ol.style.Style({
            image: new ol.style.Circle({
                radius: width * 2,
                fill: new ol.style.Fill({color: blue}),
                stroke: new ol.style.Stroke({
                    color: white, width: width / 2
                })
            })
        })
    ],
        style['position_history'] = [
            new ol.style.Style({
                image: new ol.style.Circle({
                    radius: width * 2,
                    fill: new ol.style.Fill({color: red}),
                    stroke: new ol.style.Stroke({
                        color: white, width: width / 2
                    })
                })
            })
        ];

    return style[feature.get('feature_type')];
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
var hoverInteraction = new ol.interaction.Select({
    condition: ol.events.condition.pointerMove,
    layers: [argoFloatsLayer]
});

map.addInteraction(hoverInteraction);
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

    if (feature) {
        var properties = feature.getProperties(),
            identifier = properties['identifier'],
            tooltip_text;

        if (feature.get("feature_type") === 'latest_position') {
            var last_seen = new Date(Date.parse(properties['last_seen'])).toDateString();

            tooltip_text = '<strong>' + identifier + '</strong>' + '</br>' + last_seen;
        }
        else if (feature.get("feature_type") === 'position_history') {
            var transfer_date = new Date(Date.parse(properties['timestamp'])).toDateString(),
                transfer_number = properties['transfer_number'];
            tooltip_text = '<strong>' + identifier + '[' + transfer_number + ']</strong>' + '</br>' + transfer_date;
        }
        info.tooltip('hide')
            .attr('data-original-title', tooltip_text)
            .tooltip('fixTitle')
            .tooltip('show');
    }
    else {
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


/* Clicking at Float */
var singleclickInteraction = new ol.interaction.Select({
    condition: ol.events.condition.singleClick,
    layers: [argoFloatsLayer]
});
map.addInteraction(singleclickInteraction);


var displayPlot = function (pixel) {
    var feature = map.forEachFeatureAtPixel(pixel, function (feature, layer) {
        return feature;
    });
    var img = new Image();
    var div = document.getElementById('chart-picture');
    var width = div.offsetWidth;

    div.innerHTML = '';

    if (feature && feature.getGeometry().getType() === 'Point') {
        var identifier = feature.getProperties()['identifier'];


        img.onload = function () {
            div.appendChild(img);
        };

        img.src = '/chart/' + identifier;
        img.width = width;
        img.classList.add('img-responsive');
    }
};


var positionLayer;

function displayPositions(pixel) {
    var feature = map.forEachFeatureAtPixel(pixel, function (feature, layer) {
        return feature;
    });

    if (positionLayer) {
        map.removeLayer(positionLayer);
    }

    if (feature && feature.getGeometry().getType() === 'Point') {
        var identifier = feature.get('identifier');

        var url = '/positions/' + identifier;


        positionLayer = new ol.layer.Vector({
            style: FloatStyle,
            source: new ol.source.Vector({
                format: new ol.format.GeoJSON(),
                url: url
            })
        });

        map.addLayer(positionLayer);
        console.log(positionLayer);
    }

}

map.on('click', function (evt) {
    displayPlot(map.getEventPixel(evt.originalEvent));
    displayPositions(map.getEventPixel(evt.originalEvent))
});