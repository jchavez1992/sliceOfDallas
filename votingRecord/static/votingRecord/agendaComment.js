document.addEventListener('DOMContentLoaded', function () {

	// When the form is submitted, load the callback function
	document.querySelector('#agenda_form').addEventListener('submit', (event) => addComment(event));

});

function addComment(event){
	event.preventDefault();

	const text = document.querySelector('#agenda_comment').value;
	const agendaID = document.querySelector('#agenda_id').innerText;
	const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
	const name = document.querySelector('input[name="username"]').value;

	fetch('post_comment', {
		method: 'POST',
		headers: {
			'X-CSRFToken': token
		},
		body: JSON.stringify({
			agenda_id: agendaID,
			content: text,
			username: name
		})
	})
		.then(response => response.json())
		.then(result => {
			console.log(`result is ${result.message}`)
			let commentList = document.querySelector('#comment_list');
			let new_comment = document.createElement('div');
			new_comment.className = "post_div list-group-item list-group-item-action"
			new_comment.innerText = text;
			commentList.appendChild(new_comment);
		})
		.catch(error => console.log(`error from posting new comment: ${error}`))

}