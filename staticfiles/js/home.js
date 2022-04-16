mapboxgl.accessToken = 'my_token';

document.getElementById('location_input').value = 'DUBLIN AIRPORT'
document.getElementById('location_name').value = 'Dublin'
var user_coords = []

//Bounds for map widget - user cannot scroll outside of area
const bounds = [
    [-10.91679687500000, 51.21909462044748],
    [-5.2178710937500004, 55.74334992410525]
];

//Station coordinates lat then lon
const coords = [
    ['MALIN HEAD', 55.372 , -7.339],
    ['BIRR', 53.035, -8.009],
    ['CLONES', 54.051, -7.310],
    ['BELMULLET', 54.228, -10.007],
    ['VALENTIA OBSERVATORY', 51.938, -10.241],
    ['DUBLIN AIRPORT', 53.428 , -6.241],
]

//Function for getting distance to station
function getDistance(user_coords) {
    var distance_list = []
    distance_list = coords.map(num => [num[0], Math.sqrt( Math.pow((num[1]-user_coords[0]), 2) + Math.pow((num[2]-user_coords[1]), 2) ) ])
    distance_list.sort((d1, d2) => d1[1] - d2[1])
    return distance_list[0][0]
}

//Map widget - map search box - handle user location
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/shaner13/ckwuulbsj32fh14pb195g39y2', // style URL
    center: [-6.284179687500001, 53.31774904749089], // starting position [lng, lat]
    zoom: 1, // starting zoom
    maxBounds: bounds
});

const marker = new mapboxgl.Marker({
        draggable: true,
        color: 'green',
})
.setLngLat([ -6.241, 53.428 ])//dublin
.addTo(map);

async function onDragEnd() {
    const lngLat = marker.getLngLat();
    let coords = [lngLat.lat, lngLat.lng]
    let address = await getAddressString(coords)
    document.getElementById('location_box').innerHTML = "Selected Location: ".concat(address)
    document.getElementById('location_name').value = address
    user_station = getDistance(coords)
    document.getElementById('location_input').value = user_station
}
     
marker.on('dragend', onDragEnd);

const geolocate = new mapboxgl.GeolocateControl({
    positionOptions: {
        enableHighAccuracy: true
    },
    // When active the map will receive updates to the device's location as it changes.
    trackUserLocation: true,
    // Draw an arrow next to the location dot to indicate which direction the device is heading.
    showUserHeading: true,
    showUserLocation: false,
})
map.addControl(geolocate);

geolocate.on('geolocate', async function(e) {
    let lng = e.coords.longitude;
    let lat = e.coords.latitude
    marker.setLngLat([lng, lat])
    let address = await getAddressString([lat, lng])
    document.getElementById('location_box').innerHTML = "Selected Location: ".concat(address)
    document.getElementById('location_name').value = address
    user_station = getDistance([lat, lng])
    document.getElementById('location_input').value = user_station
});

map.on('click', async (e) => {
    user_coords = [e.lngLat.wrap().lat, e.lngLat.wrap().lng]
    let address = await getAddressString(user_coords)
    user_station = getDistance(user_coords)
    document.getElementById('location_input').value = user_station
    document.getElementById('location_name').value = address
    document.getElementById('location_box').innerHTML = "Selected Location: ".concat(address)
    marker.setLngLat([e.lngLat.wrap().lng, e.lngLat.wrap().lat])
});

async function getAddressString(coords) {
    let response = await fetch('https://api.mapbox.com/geocoding/v5/mapbox.places/'.concat(coords[1].toFixed(2)).concat(',').concat(coords[0].toFixed(2))
    .concat('.json?access_token=pk.eyJ1Ijoic2hhbmVyMTMiLCJhIjoiY2t3dWs1czdiMXF5cjJwcDM2YzVhcDU2MSJ9.aei6jzpMUqS3LJ2_k6dAqw'));
    let data = await response.json()
    return data['features'][0]['place_name'];
}

var slider = document.getElementById("slider");
var output = document.getElementById("slider-output");

output.innerHTML = slider.value; 
output.innerHTML = slider.value.concat(" KwP")

slider.oninput = function() {
  output.innerHTML = this.value.concat(" KwP")
} 
