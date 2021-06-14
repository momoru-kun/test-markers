async function fetchPicture(viewer, id = null) {
    let promise = null
    if (id === null) {
        promise = fetch('/picture');
    } else {
        promise = fetch('/picture?id=' + id);
    }
    let data = await response.json();

    let markersPlugin = viewer.getPlugin(PhotoSphereViewer.MarkersPlugin);
    data.markers.forEach(marker => {
        markersPlugin.clearMarkers();
        viewer.setPanorama(data.picture);
        viewer.setOption('caption', data.name);
        viewer.rotate({
            longitude: 0, 
            latitude: 0
        })
        data.markers.forEach(marker => {
            markersPlugin.addMarker({
                id: marker.to,
                circle: 20,
                x: marker.position[0],
                y: marker.position[1],
                tooltip: marker.text
            })
        })
    })
    document.querySelector('div#image_description').innerHTML = data.description
}

document.addEventListener('DOMContentLoaded', async () => {
    let viewer = new PhotoSphereViewer.Viewer({
        container: 'sphere',
        loadingImg: 'https://photo-sphere-viewer.js.org/assets/photosphere-logo.gif',
        plugins: [
            [PhotoSphereViewer.MarkersPlugin, {markers}]
        ]
    });
    await fetchPicture(viewer);
    
    markersPlugin.on( 'select-marker', async ( _, marker ) => {
        await fetchPicture(viewer, id = marker.id);
    })

    document.querySelector('div#comment_btn').addEventListener('onclick', () => {
        document.querySelector('div#more').classList.toggle('opened')
    })
})