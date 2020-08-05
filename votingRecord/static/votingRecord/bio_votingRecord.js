document.addEventListener('DOMContentLoaded', function () {

	// When the button clicked, show voting record below bio.
	document.querySelector('#show_vr').addEventListener('submit', (event) => showVR(event));

});

function showVR(event){

	const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

}