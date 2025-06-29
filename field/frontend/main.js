
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


	const { values, deck, is_dark } = event.detail.args;
	const dark_prefix = is_dark ? 'dark-' : 'light-';
	const black_class = dark_prefix + 'black';
	const red_class = dark_prefix + 'red';


	const field = document.getElementById('touche-field');
	values.forEach((value, index) => {
		const cell = document.createElement('div');
		const text = get_text(value);
		cell.textContent = text;

		if (value == Field.FreeSpace) cell.classList.add('free-cell', black_class);
		else if (text.length > 0)
			cell.classList.add('card-cell', value < Deck.redUntilIndex ? red_class : black_class);
		else cell.classList.add('empty-cell');

		if (text.length > 0) cell.onclick = () =>
			Streamlit.setComponentValue({ x: index % 12, y: index / 12 >> 0 })

		field.appendChild(cell);
	})


	const cards = document.getElementsByClassName('card');
	deck.forEach((value, index) => {
		const card = cards[index];
		card.textContent = get_text(value);
		card.classList.add(value < Deck.redUntilIndex ? red_class : black_class);
	})

	const { width, height } = document.body.getBoundingClientRect();
	Streamlit.setFrameHeight(height)
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(-1)