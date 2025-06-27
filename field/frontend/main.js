
function sendValue(value) {
 	Streamlit.setComponentValue(value)
}

function onRender(event) {
	if (window.rendered) return
	else window.rendered = true

	const {label, value} = event.detail.args;

	const label_el = document.getElementById("label")
	label_el.innerText = label

	const input = document.getElementById("input_box");
	if (value) {
	  input.value = value
	}

	input.onkeyup = event => sendValue(event.target.value)
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(100)