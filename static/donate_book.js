var fileinput = document.getElementById('fileinput');
var imageSize = document.getElementById('imageSize');

fileinput.onchange = function(){
	const file = fileinput.files[0];

	if(!file) 
		return;
	
	const fsize = Math.round((file.size/1024));

	imageSize.innerHTML = "Image size: " + (fsize/1024).toFixed(2) + "MB."
}

function validateForm() {
	const file = fileinput.files[0];
	
	if(!file) 
		return;
	
	const fsize = Math.round((file.size/1024));

	if(fsize >4096){
		alert("Image is too big. Maximum size of image can be 4MB.");
		return false;
	}
	else{
		return true;
	}
}