document.addEventListener('DOMContentLoaded', function () {

	// Use buttons to toggle between views
	document.querySelector('#agenda_form').addEventListener('submit', () => loadMailbox('inbox'));

	// By default, load the inbox
	loadMailbox('inbox');
});