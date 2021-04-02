var fileinput = document.getElementById('fileinput');
var imageSize = document.getElementById('imageSize');

fileinput.onchange = function(){
	const file = fileinput.files[0];

	if(!file) 
		return;
	
	const fsize =file.size/1024;

	imageSize.innerHTML = "Image size: " + fsize.toFixed(2) + "KB."
}

function validateForm() {
	const file = fileinput.files[0];
	
	if(!file) 
		return;
	
	const fsize = Math.round((file.size/1024));

	if(fsize >500.05){
		alert("Image is too big. Maximum size of image can be 500KB.");
		return false;
	}
	else{
		return true;
	}
}