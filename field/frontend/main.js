
function onRender(event) {
	if (window.rendered) return
	else window.rendered = true


	const { values } = event.detail.args;

	const field = document.getElementById("touche-field");

	values.forEach(value => {
		const cell = document.createElement("div");
		cell.classList.add("cell");
		if (value == 'free\nspace') cell.classList.add("free-space");
		else if (value.length > 0) {
			cell.classList.add("card");
			if (value.includes('♥') || value.includes('♦'))
				cell.classList.add("red-card");
		}
		cell.textContent = value;
		field.appendChild(cell);
	})


	const { width, height } = document.body.getBoundingClientRect();
	Streamlit.setFrameHeight(height)
	Streamlit.setComponentValue(height)


	/*const {label, value} = event.detail.args;

	const label_el = document.getElementById("label");
	label_el.innerText = label;

	const input = document.getElementById("input_box");
	if (value) {
	  input.value = value
	}

	input.onkeyup = event => sendValue(event.target.value)*/
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(-1)