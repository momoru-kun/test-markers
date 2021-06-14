var retypeComment = false

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function appendComment(email, text) {
    let container = document.querySelector('div#comment_section');
    console.log(container.innerHTML)
    let emptyContainerString = '<div class="comment_empty">Тут как-то путовато...<br>Разбавь пустоту своим коментарием!</div>'
    if (container.innerHTML == emptyContainerString) {
        container.innerHTML = ""
    } 

    let card = document.createElement('div');
    card.classList.add('comment_card')
    card.innerHTML = `<div class="card_title">${email}`+
        `</div><div class="card_text">${text}</div>` 
    container.appendChild(card)
}

function sendComment(image_id, email, text) {
    if (image_id === undefined) { console.error('Image id is null'); return }
    if (email === undefined) { console.error('Email is null'); return }
    if (text === undefined) { console.error('Text is null'); return }
    
    let valid = true
    const re = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    if (!re.test(String(email).toLowerCase())) {
        document.querySelector('input[name="email"]').classList.add('errored');
        document.querySelector('div#email_error').classList.add("visible");
        valid = false;
    }
    if (text.length <= 16) {
        document.querySelector('textarea[name="text"]').classList.add('errored');
        document.querySelector('div#text_error').classList.add("visible");
        valid = false;
    }

    if (!valid) return;

    fetch('/comment/', {
        method: 'POST',
        credentials : 'same-origin',
        body: JSON.stringify({
            id: image_id,
            email: email,
            text: text,
            csrfmiddlewaretoken: window.csrftoken
        }),
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    }).then(response => {
        if (response.status != 200) console.error(response.data);
        else appendComment(email, text);
    })
}

async function getComments(image_id) {
    let response = await fetch(`/comment?id=${ image_id }`);
    let data = await response.json();

    let container = document.querySelector('div#comment_section');
    container.innerHTML = '';
    if (data.result.length == 0) {
        container.innerHTML = '<div class="comment_empty">Тут как-то путовато...<br/>' + 
        'Разбавь пустоту своим коментарием!</div>';
        return;
    }
    data.result.forEach(comment => {
        appendComment(comment.email, comment.text)
    })
}

async function fetchPicture(viewer = null, id = null) {
    let promise = null
    if (id === null) {
        promise = await fetch('/picture');
    } else {
        promise = await fetch('/picture?id=' + id);
    }
    let data = await promise.json();

    document.querySelector('div#image_description').innerHTML = data.description

    let _viewer;
    if (viewer === null) {
        let markers = []
        data.markers.forEach(marker => {
            markers.push({
                id: marker.to,
                circle: 20,
                x: marker.position[0],
                y: marker.position[1],
                tooltip: marker.text
            })
        })
        _viewer = new PhotoSphereViewer.Viewer({
            container: 'sphere',
            caption: data.name,
            panorama: data.picture,
            loadingImg: 'https://photo-sphere-viewer.js.org/assets/photosphere-logo.gif',
            plugins: [
                [PhotoSphereViewer.MarkersPlugin, {markers}]
            ]
        });
    } else {
        updatePicture(viewer, data)
        return {id: data.id}
    }
    

    if (id === null) {
        return {viewer: _viewer, id: data.id}
    }
}

function updatePicture(viewer, data) {
    getComments(data.id)
    document.querySelector('div#image_description').innerHTML = data.description
    let markersPlugin = viewer.getPlugin(PhotoSphereViewer.MarkersPlugin);
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
}

function hideMenu() {
    document.querySelector('div#sphere').removeEventListener('click', hideMenu)
    document.querySelector('div#more').classList.toggle('opened')
}

document.addEventListener('DOMContentLoaded', async () => {
    let data = await fetchPicture();
    let viewer = await data.viewer;
    let image = await data.id ;
    
    let markersPlugin = viewer.getPlugin(PhotoSphereViewer.MarkersPlugin);
    
    markersPlugin.on( 'select-marker', async ( _, marker ) => {
        data = await fetchPicture(viewer, id = marker.id);
        image = await data.id;
    })

    getComments(image)

    document.querySelector('div#comment_btn').addEventListener('click', () => {
        document.querySelector('div#sphere').addEventListener('click', hideMenu);
        document.querySelector('div#more').classList.toggle('opened');
    })

    document.querySelector('textarea[name="text"]').addEventListener('input', () => {
        document.querySelector('textarea[name="text"]').classList.remove('errored');
        document.querySelector('div#text_error').classList.remove("visible");
    })
    document.querySelector('input[name="email"]').addEventListener('input', () => {
        document.querySelector('input[name="email"]').classList.remove('errored');
        document.querySelector('div#email_error').classList.remove("visible");
    })

    document.querySelector('input#send_comment').addEventListener('click', event => {
        event.preventDefault();
        let text = document.querySelector('textarea[name="text"]').value
        let email = document.querySelector('input[name="email"]').value
        sendComment(image, email, text)
    })
})