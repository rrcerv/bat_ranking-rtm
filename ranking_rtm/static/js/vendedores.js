import 'https://unpkg.com/face-api.js@0.22.2/dist/face-api.min.js'

function uploadPhotoEventListener(photoInput){
    const uploadFileButton = document.getElementById('uploadFileButton');

    uploadFileButton.addEventListener('click', (event) =>{
        photoInput.click();
    })
}

function getCookie(name){
    var cookieValue = null;

    if(document.cookie && document.cookie != ''){
        var cookies = document.cookie.split(';')

        for(var i=0;i<cookies.length;i++){
            var cookie = cookies[i].trim()

            if(cookie.substring(0, name.length+1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))

                break
            }
        }

    }

    return cookieValue
}

function validateFileExtension(userInput){
    // SOMENTE PERMITIDAS AS EXTENSÕES PNG, JPG, JPEG E WEBP
    var fileName = userInput.name;
    var splittedName = fileName.split('.')
    var extension = splittedName[splittedName.length-1].toLowerCase()
    
    if (extension=='png' || extension =='jpg' || extension== 'jpeg' || extension == 'webp'){
        return true;
    } else {
        return false;
    }
}

function getBase64(file) {
    if(file){
    return new Promise((resolve, reject) => {
        var reader = new FileReader();
    
        reader.readAsDataURL(file);
    
        reader.onload = function () {
            resolve(reader.result);
        };
    
        reader.onerror = function (error) {
            reject(error);
        };
    });
    } else{
        return ''
    }

 }

export default function loadImage(imgURL) {
    const image = new Image();

    image.crossOrigin = true;

    return new Promise((resolve, reject) => {
        image.addEventListener('error', (error) => reject(error));
        image.addEventListener('load', () => resolve(image));

        image.src = imgURL;
    });
};

function fetchPhotoApi(results, base64Photo, AI){
        var boundingResults = results[0];
        
        // AMARRANDO RESULTADOS EM JSON PARA ENVIAR PARA API
        if(AI){
            var formData = {
                userImage: base64Photo, 
                boundingBox: {
                    bottom: boundingResults.box.bottom,
                    left: boundingResults.box.left*0.50,
                    top: boundingResults.box.top*0.8,
                    right: boundingResults.box.right*1.15
                }
            }
        } else{
            var formData = {
                userImage: base64Photo, 
                boundingBox: {
                    bottom: boundingResults.box.bottom,
                    left: boundingResults.box.left,
                    top: boundingResults.box.top,
                    right: boundingResults.box.right
                }
            }
        }


        var headers = {
                'X-CSRFToken' : getCookie('csrftoken') 
            }

        // ENVIANDO PARA API
        fetch(`${ApiUrl}`, {
            method: 'POST', 
            body: JSON.stringify(formData),
            headers: headers
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            window.location = window.location.href+`?plKfris=${randomNumber}`
        })
        .catch(error => {
            alert('Algo deu errado. Por favor, tente novamente.')
            console.error('There was a problem with the image upload:', error);
            // Handle error
        });

}

function setCropModal(imgURL, base64Photo){
    const modalCropPhotoElement = document.getElementById('modalCropPhoto');
    var modalCropPhoto = new bootstrap.Modal(modalCropPhotoElement)
    var cropPhotoInput = document.getElementById('cropPhotoInput');
    var uploadCroppedImgBtn = document.getElementById('uploadCroppedImgBtn');
    cropPhotoInput.src = imgURL;
    modalCropPhoto.show()

    var width = cropPhotoInput.width;
    var heigth = cropPhotoInput.heigth;

    const cropper = new Cropper(cropPhotoInput, {
      aspectRatio: 16 / 16,
      zoomable: false,
      viewMode:1,
      movable: false,
    });
                    
    uploadCroppedImgBtn.addEventListener('click', (event) => {
        console.log(cropper.getCropBoxData())
        //var cropBoxData = cropper.getCropBoxData();
        var cropBoxdata = cropper.getData();
        console.log(cropBoxdata);
        var cropperCanvas = document.querySelector('.cropperPhoto')
        var originalWidth = cropPhotoInput.naturalWidth;
        var originalHeight = cropPhotoInput.naturalHeight;
        
        //console.log('CropBoxDataLeft', cropBoxData.left)
        //console.log('Top', cropBoxData.top)
        //console.log('OriginalHeight', originalHeight, 'CropboxHeight', cropBoxData.height, 'CropPhotoInputHeight', cropperCanvas.offsetHeight, 'CropBoxDataTop', cropBoxData.top);
        //console.log('cropboDataWidth', cropBoxData.width, 'originalWidth', originalWidth, 'cropPhotoInputWidth', cropperCanvas.offsetWidth, 'cropBoxDataLeft', cropBoxData.left);

        //var json = {
        //        0: {
        //            box:{
        //                left: ( ( cropBoxData.left / cropperCanvas.offsetWidth ) * originalWidth ),
        //                top: ( ( cropBoxData.top / cropperCanvas.offsetHeight ) * originalHeight ) ,
        //                bottom: ( (originalHeight*cropBoxData.height) / cropperCanvas.offsetHeight) + ( ( cropBoxData.top / cropperCanvas.offsetHeight ) * originalHeight ) ,
        //                right: ( (cropBoxData.width*originalWidth) /cropperCanvas.offsetWidth) + ( ( cropBoxData.left / cropperCanvas.offsetWidth ) * originalWidth )
        //            }
        //        }
        //    }
//
        //    fetchPhotoApi(json, base64Photo)
        //})
        
        console.log(cropBoxdata.x, cropBoxdata.y, cropBoxdata.height, cropBoxdata.width)

        var json = {
                0: {
                    box:{
                        left: cropBoxdata.x,
                        top: cropBoxdata.y,
                        bottom: cropBoxdata.y + cropBoxdata.height,
                        right: cropBoxdata.x + cropBoxdata.width
                    }
                }
            }
            
            console.log('JSON', json);
            fetchPhotoApi(json, base64Photo, false)
        });

}

function resizeImage(img){

    const maxWidth = 500
    const maxHeight = 500

    const ratio = img.width / img.height

    var newWidth, newHeight;

    if (img.width > maxWidth){
        
        newWidth = maxWidth
        newHeight = newWidth / ratio

    } else if (img.height > maxHeight){

        newHeight = maxHeight
        newWidth = ratio * newHeight

    } else{
        newHeight = img.height;
        newWidth = img.width;
    }

    let canvas = document.createElement('canvas');
    canvas.width = newWidth;
    canvas.height = newHeight;
    let ctxt = canvas.getContext('2d');
    ctxt.drawImage(img, 0, 0, newWidth, newHeight);


    return [canvas.toDataURL(), canvas]; 

}

await faceapi.nets.tinyFaceDetector.loadFromUri(`${urlModels}`);
const photoInputElement = document.getElementById('photoInput');


uploadPhotoEventListener(photoInputElement);

photoInputElement.addEventListener('change', (event) => {
    var photoInput = photoInputElement.files[0];

    // PROCESSAMENTO DA IMAGEM AQUI -- Foto vai precisar ser extraída em Base64

    if (validateFileExtension(photoInput)) {
        getBase64(photoInput)
            .then((data) => {

                var base64Photo = data;
                console.log(photoInput);

                let imgURL = URL.createObjectURL(photoInput);
                const imgElement = new Image();
                imgElement.src = imgURL;

                var newBase64, canvasElement;

                imgElement.addEventListener('load', (event) => {
                    var resizedImageData = resizeImage(imgElement);

                    newBase64 = resizedImageData[0];
                    canvasElement = resizedImageData[1];

                    canvasElement.toBlob((blob) => {

                        var newFileReader = new FileReader();

                        var newURL = URL.createObjectURL(blob)

                        faceapi.detectAllFaces(
                            canvasElement, // imgElemente
                            new faceapi.TinyFaceDetectorOptions(),
                        ).then(results => {

                            if (results.length == 1) {
                                // SE TIVER UMA FACE DETECTADA NA FOTO
                                fetchPhotoApi(results, newBase64, true);
                            } else {
                                // SE TIVER MAIS DE UMA OU NENHUMA FACE DETECTADA || imgURL
                                setCropModal(newURL, newBase64);
                            }

                        })

                    })




                })


            })
    } else {
        alert('Formato não permitido');
    }
})


