// Setup code

let imageOpsElem = document.getElementById('image-ops');
let slider = document.getElementById("slider");
slider.style.visibility = "hidden";
let sliderOutput = document.getElementById("slider-output");
console.log('hi', sliderOutput);

imageOpsElem.addEventListener('change', e => {
    console.log(e.target.value);
    let imgOp = e.target.value;
    if(imgOp.includes("enhance")){
        slider.style.visibility = "visible";
        slider.min = 0;
        slider.max = 100;
        slider.value = 50;
        slider.range = 3;
        slider.scaledValue = slider.value * slider.range / (slider.max - slider.min);
        sliderOutput.innerHTML = slider.scaledValue;
    }
    else{
        slider.style.visibility = "hidden";
        sliderOutput.innerHTML = "";
    }
})

slider.addEventListener("input", e => {
    let value = e.target.value;
    slider.scaledValue = slider.range * value / (slider.max - slider.min);
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
        form_data.append('mag', slider.scaledValue);
        $.ajax({
            type: 'POST',
            url: '/uploadsingle',
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

// 