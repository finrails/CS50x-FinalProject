const getTasks = async post_id => {
	const responsePromise = await fetch(`/tasks/${post_id}`, { method: 'DELETE' })
	const freshHTML = await responsePromise.text()
	
	if (responsePromise.ok) {
		root = document.querySelector("#root")
		root.innerHTML = freshHTML
	}

}
