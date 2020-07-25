const previewImagesBlock = document.getElementById('preview-block');

// js drag and drop
var draggedBlock = null;

const dragStart = e => {
    draggedBlock = e.target;
}

const dropped = e => {
    cancelDefault(e);
    var targetBlock = e.target;
    $(draggedBlock).insertBefore(targetBlock);
}

const cancelDefault = e => {
    e.preventDefault();
    e.stopPropagation();
    return false;
}

// Create image block
const createImagePreviewBlock = (id, src)=> {

    let img = document.createElement('img');
    img.id = `preview-image-${id}`;
    img.alt = "uploaded image";
    img.src = src;
    img.className = "preview-image";

    img.setAttribute("draggable", true);
    img.addEventListener('dragstart', dragStart);
    img.addEventListener('drop', dropped);
    img.addEventListener('dragenter', cancelDefault);
    img.addEventListener('dragover', cancelDefault);

    return img;
}

// clear preview images 
const clearImagePreviewBlocks = () => {
    while(previewImagesBlock.firstChild){
        previewImagesBlock.removeChild(previewImagesBlock.lastChild);
    }
}

// Return the image file orderings after shuffle using drag drop
const getImageBlockOrdering = () => {
    let blocks = document.getElementsByClassName('preview-image');
    let blockIds = Array.from(blocks).map(elem => parseInt(elem.id.split('-').pop()));
    return blockIds;
}

// jQuery + ajax upload file
$(function() {
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        var mimetype = document.getElementById("upload-file-input").files[0].type;
        console.log(mimetype);
        let ordering = getImageBlockOrdering();
        form_data.append('order', ordering);
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                document.getElementById("result-preview").src = `data:${mimetype};base64,` + data;
                console.log(data);
            },
        });
    });
});

// read multiple image as data urls, and set preview image source
const readDataUrl = input => {
    if(input.files && input.files[0]){
        console.log(input.files);
        for(let i = 0; i < input.files.length; ++i){
            var reader = new FileReader();
            reader.onload = e => {
                let div = createImagePreviewBlock(i, e.target.result);
                previewImagesBlock.appendChild(div);
            }
            reader.readAsDataURL(input.files[i]);
        }
    }
}

// jQuery detect input image onchange
$(function(){
    $("#upload-file-input").change(function(){
        console.log("input file change");
        clearImagePreviewBlocks();
        readDataUrl(this);
    });
})