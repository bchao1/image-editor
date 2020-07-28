const previewImagesBlock = document.getElementById('preview-block');

// Create image block
const createImagePreviewBlock = (id, src)=> {
    let div = document.createElement('div');
    div.className = 'preview-image-div';

    let img = document.createElement('img');
    img.id = `preview-image-${id}`;
    img.alt = "uploaded image";
    img.src = src;

    div.appendChild(img);
    return div;
}

// clear preview images 
const clearImagePreviewBlocks = () => {
    while(previewImagesBlock.firstChild){
        previewImagesBlock.removeChild(previewImagesBlock.lastChild);
    }
}

// jQuery + ajax upload file
$(function() {
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        var mimetype = document.getElementById("upload-file-input").files[0].type;
        console.log(mimetype);
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

// read (single) image as data url, and set preview image source
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
