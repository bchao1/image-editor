// jQuery + ajax upload file
$(function() {
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        var mimetype = document.getElementById("upload-file-input").files[0].type;
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

// read image as data url, and set preview image source
const readDataUrl = input => {
    if(input.files && input.files[0]){
        var reader = new FileReader();
        reader.onload = e => {
            document.getElementById("upload-preview").src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// jQuery detect input image onchange
$(function(){
    $("#upload-file-input").change(function(){
        console.log("input file change");
        readDataUrl(this);
    });
})