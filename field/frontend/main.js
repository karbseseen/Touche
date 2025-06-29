
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

function initRender(event) {
	const { field_data, dot_color } = event.detail.args;


	const field = document.getElementById('touche-field');
	field_data.forEach((value, index) => {
		const cell = document.createElement('div');
		const text = get_text(value);
		cell.textContent = text;

		cell.classList.add('cell');
		if (value == Field.FreeSpace) cell.classList.add('free-cell', 'light-bg', 'light-text');
		else if (text.length > 0)
			cell.classList.add('card-cell', 'light-bg', value < Deck.redUntilIndex ? 'red-text' : 'light-text');
		else cell.classList.add('empty-cell');

		if (text.length > 0) cell.onclick = () =>
			Streamlit.setComponentValue({ x: index % 12, y: index / 12 >> 0 });

		field.appendChild(cell);
	})


	const cards = document.getElementById('deck').children;
	const card_click = (card) => () => {
		const make_selected = card.classList.contains('unselected-card');
		for (let index = 0; index < cards.length; index++) {
			cards[index].classList.remove('selected-card');
			cards[index].classList.add('unselected-card');
		}
		if (make_selected) {
			card.classList.remove('unselected-card');
			card.classList.add('selected-card');
		}
	}
	for (let index = 0; index < cards.length; index++) {
		const card = cards[index];
		card.classList.add('unselected-card');
		card.onclick = card_click(card);
	}


	const { width, height } = document.body.getBoundingClientRect();
	Streamlit.setFrameHeight(height)
}

function updateRender(event) {
	const { pressed, deck, is_dark } = event.detail.args;

	const old_bg_class = is_dark ? 'light-bg' : 'dark-bg';
	const new_bg_class = is_dark ? 'dark-bg' : 'light-bg';
	const bg_elements = document.getElementsByClassName(old_bg_class);
	while (bg_elements.length > 0) {
		bg_elements[0].classList.add(new_bg_class);
		bg_elements[0].classList.remove(old_bg_class);
	}

	const old_text_class = is_dark ? 'light-text' : 'dark-text';
	const new_text_class = is_dark ? 'dark-text' : 'light-text';
	const text_elements = document.getElementsByClassName(old_text_class);
	while (text_elements.length > 0) {
		text_elements[0].classList.add(new_text_class);
		text_elements[0].classList.remove(old_text_class);
	}


	const cards = document.getElementById('deck').children;
	deck.forEach((value, index) => {
		const card = cards[index];
		const children = cards[index].children;
		for (let child_index = 0; child_index < children.length; child_index++) {
			const child = children[child_index];
			child.textContent = get_text(value);
			child.classList.remove('red-text', 'black-text');
			child.classList.add(value < Deck.redUntilIndex ? 'red-text' : 'black-text');
		}
	});

}

function onRender(event) {
	if (!window.rendered) {
		initRender(event);
		window.rendered = true;
	}
	updateRender(event);
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(-1)