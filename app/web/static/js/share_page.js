const galleryDiv = document.getElementById("gallery");

const setup = () => {
    // Onload -> send request to backend to query all photos

    $.ajax({
        type: 'GET',
        url: '/fetch_all_images',
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            let images = data['img'];
            let extensions = data['ext'];
            Object.keys(images).forEach(function(key) {
                imageItem = createImageItem(key, images[key], extensions[key]);
                galleryDiv.appendChild(imageItem);
            });
        },
    });
}

const createImageItem = (image_id, image_data, extension) => {
    console.log(image_id, extension)
    // Image data is base64 string, image_id is the hash key in datastore
    /*
    <div class="image-item">
        <img src="/images/test.png">
        <div class="like-div">
            <img src="/images/like.png">
            <span class="like-count">26</span>
        </div>
    </div>
    */
    const imageItem = document.createElement('div');
    imageItem.className = "image-item";
    const img = document.createElement('img');
    img.src=`data:${extension};base64,` + image_data;
    imageItem.appendChild(img);
    const likeDiv = document.createElement('div');
    likeDiv.className = "like-div";
    const likeBtn = document.createElement('img');
    likeBtn.src = "/images/like.png";
    const likeCount = document.createElement('span');
    likeCount.className = "like-count";
    likeCount.innerHTML = 0;
    likeDiv.appendChild(likeBtn);
    likeDiv.appendChild(likeCount);
    imageItem.appendChild(likeDiv);
    likeBtn.addEventListener("click", e => {
        var likes = parseInt(likeCount.innerHTML) + 1;
        likeCount.innerHTML = likes;
        // Send request to backend to update likes
        // Send likes, image ID
        var data = new FormData();
        data.append("image_id", image_id); // Set image ID
        data.append("likes", likes);
        $.ajax({
            type: 'POST',
            url: '/like_image',
            data: data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log("Updated likes!");
            },
        });
    })
    return imageItem;
}