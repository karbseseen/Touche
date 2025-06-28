
function onRender(event) {
	if (window.rendered) return
	else window.rendered = true


	const { values, is_dark } = event.detail.args;

	const bg_class = is_dark ? 'dark-bg' : 'light-bg';
	const text_class = is_dark ? 'dark-text' : 'light-text';

	const field = document.getElementById("touche-field");
	values.forEach((value, index) => {
		const cell = document.createElement("div");
		cell.textContent = value;

		cell.classList.add("cell");
		if (value == 'free\nspace') cell.classList.add("free-space", bg_class, text_class);
		else if (value.length > 0) {
			const is_red = value.includes('♥') || value.includes('♦');
			const card_text_class = is_red ? 'red-text' : text_class;
			cell.classList.add("card", bg_class, card_text_class);
		}

		if (value.length > 0) cell.onclick = () =>
			Streamlit.setComponentValue({ x: index % 12, y: index / 12 >> 0 })

		field.appendChild(cell);
	})


	const { width, height } = document.body.getBoundingClientRect();
	Streamlit.setFrameHeight(height)
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(-1)