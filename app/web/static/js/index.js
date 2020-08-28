// Global accessors
let sessionID = uuidv4();
let imageOpsElem = document.getElementById('image-ops');
let slider = document.getElementById("slider"); 
let sliderOutput = document.getElementById("slider-output");
let downloadButton = document.getElementById("download-button");
let shareButton = document.getElementById("share-button");
let resultPreview = document.getElementById("result-preview");
let uploadPreview = document.getElementById("upload-preview");

const initSlider = imgOp => {
    if(imgOp.includes("enhance")){
        slider.style.visibility = "visible";
        slider.min = 0;
        slider.max = 100;
        slider.value = 50;
        slider.range = 3;
        slider.scaledValue = slider.value * slider.range / (slider.max - slider.min);
        sliderOutput.innerHTML = slider.scaledValue;
    }
    else if(imgOp.includes("quantize")){
        // Fixed levels of quantization = 256 colors
        slider.style.visibility = "visible";
        slider.min = 1;
        slider.max = 8;
        slider.value = 5;
        slider.scaledValue = parseInt(Math.pow(2, slider.value));
        sliderOutput.innerHTML = slider.scaledValue;
    }
    else{
        slider.style.visibility = "hidden";
        sliderOutput.innerHTML = "";
    }
}

// read (single) image as data url, and set preview image source
const readDataUrl = input => {
    if(input.files && input.files[0]){
        console.log(input.files);
        var reader = new FileReader();
        reader.onload = e => {
            uploadPreview.style.height = null;
            uploadPreview.src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// jQuery detect input image onchange
$(function(){
    $("#upload-file-input").change(function(){
        console.log("input file change");
        readDataUrl(this);
        resultPreview.src = "none";
    });
})

// Initialization code

const setup = () => {
    uploadPreview.style.height = "40vh";
    resultPreview.style.height = "40vh";
    // Init slider
    var selected_op = imageOpsElem.options[imageOpsElem.selectedIndex].value;
    initSlider(selected_op);

    imageOpsElem.addEventListener('change', e => {
        console.log(e.target.value);
        let imgOp = e.target.value;
        initSlider(imgOp);
    })
    
    slider.addEventListener("input", e => {
        let value = e.target.value;
        let selected_op = imageOpsElem.options[imageOpsElem.selectedIndex].value;
        if(selected_op.includes("enhance")){
            slider.scaledValue = slider.range * value / (slider.max - slider.min);
        }
        else if(selected_op.includes("quantize")){
            slider.scaledValue = parseInt(Math.pow(2, slider.value));
        }
        sliderOutput.innerHTML = slider.scaledValue;
    })
    // jQuery + ajax upload file
    $(function() {
        $('#upload-file-btn').click(function() {
            var form_data = new FormData($('#upload-file')[0]);
            var mimetype = document.getElementById("upload-file-input").files[0].type;
            console.log(mimetype);
            var selected_op = imageOpsElem.options[imageOpsElem.selectedIndex].value;
            console.log(selected_op);
            form_data.append('op', selected_op);
            form_data.append('mag', slider.scaledValue | 0); // guard undefined
            form_data.append('sess', sessionID); // session id
            //form_data.append('image_data', resultPreview.src) // also send processed result. First time = null
            $.ajax({
                type: 'POST',
                url: '/uploadsingle',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    resultPreview.style.height = null;
                    resultPreview.src = `data:${mimetype};base64,` + data;
                    downloadButton.href = `data:${mimetype};base64,` + data
                    downloadButton.download = `test.${mimetype.split('/')[1]}`; // get file extension
                },
            });
        });
    });

    $(function(){
        $("#share-button").click(function(){
            console.log("Share");
            var form_data = new FormData();
            form_data.append("image_data", resultPreview.src);
            form_data.append("image_id", uuidv4());
            $.ajax({
                type: "POST",
                url: '/shareimage',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    console.log(data)
                }
            });
        });
    });

    $(function(){
        $("#undo-btn").click(function(){
            var form_data = new FormData();
            form_data.append("sess", sessionID)
            $.ajax({
                type: "POST",
                url: '/undo-op',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    console.log(data)
                }
            })
        })
    })

    $(function(){
        $("#redo-btn").click(function(){
            var form_data = new FormData();
            form_data.append("sess", sessionID)
            $.ajax({
                type: "POST",
                url: '/redo-op',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    console.log(data)
                }
            })
        })
    })
}