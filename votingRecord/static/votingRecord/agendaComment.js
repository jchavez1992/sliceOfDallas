document.addEventListener('DOMContentLoaded', function () {

	// When the form is submitted, load the callback function
	document.querySelector('#agenda_form').addEventListener('submit', (event) => addComment(event));

});

function addComment(event){
	event.preventDefault();

	const text = document.querySelector('#agenda_comment').value;
	const agendaID = document.querySelector('#agenda_id').innerText;
	const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

	fetch('/post_comment', {
		method: POST,
		headers: {
			'X-CSRFToken': token
		},
		body: JSON.stringify({
			agenda_id: agendaID,
			content: text
		})
	})
		.then(response => response.json())
		.then(result => console.log(`New comment posted: ${result}`))
		.catch(error => console.log(`error from posting new comment: ${error}`))

}