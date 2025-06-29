
const Deck = {
  size: 53,
  numbers: ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
  suits: ['♥', '♦', '♣', '♠'],
  redUntilIndex: 26,
  Joker: 52,
};
const Field = { FreeSpace: Deck.size };
function get_text(card_index) {
	if (card_index < 0 || card_index > Deck.size) return '';
	else if (card_index == Deck.Joker) return 'Joker';
	else if (card_index == Field.FreeSpace) return 'free\nspace';
	else return Deck.numbers[card_index % Deck.numbers.length] + '\n' +
		Deck.suits[card_index / Deck.numbers.length >> 0];
}

function onRender(event) {
	if (window.rendered) return
	else window.rendered = true


	const { field_data, pressed, deck, selected_card, is_dark, dot_color } = event.detail.args;
	const bg_class = is_dark ? 'dark-bg' : 'light-bg';


	const field = document.getElementById('touche-field');
	field_data.forEach((value, index) => {
		const cell = document.createElement('div');
		const text = get_text(value);
		cell.textContent = text;

		cell.classList.add('cell');
		if (value == Field.FreeSpace) cell.classList.add('free-cell', bg_class, 'black-text');
		else if (text.length > 0)
			cell.classList.add('card-cell', bg_class, value < Deck.redUntilIndex ? 'red-text' : 'black-text');
		else cell.classList.add('empty-cell');

		if (text.length > 0) cell.onclick = () =>
			Streamlit.setComponentValue({ x: index % 12, y: index / 12 >> 0 });

		field.appendChild(cell);
	})

	const cells = document.getElementsByClassName('cell');
	pressed.forEach(index => {
		const cell = cells[Math.abs(index)];
		const dot = document.createElement('span');
		dot.classList.add(index > 0 ? 'dot' : 'final-dot');
	});

	const cards = document.getElementById('deck').children;
	deck.forEach((value, index) => {
		const card = cards[index];

		const children = cards[index].children;
		for (let child_index = 0; child_index < children.length; child_index++) {
			const child = children[child_index];
			child.textContent = get_text(value);
			child.classList.add('white-bg', value < Deck.redUntilIndex ? 'red-text' : 'black-text');
		}

		card.onclick = () => Streamlit.setComponentValue({ card: index });
	});


	const { width, height } = document.body.getBoundingClientRect();
	Streamlit.setFrameHeight(height)
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(-1)