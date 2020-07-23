// jQuery + ajax upload file
$(function() {
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        var input_file = document.getElementById("upload-file-input").files[0];
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                var reader = new FileReader();
                reader.onload = e => {
                    document.getElementById("result-preview").src = e.target.result;
                };
                console.log('filetype', input_file.type);
                reader.readAsDataURL(new Blob([data], { type: input_file.type }));
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