
const Deck = {
	size: 53,
	numbers: ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
	suits: ['♥', '♦', '♣', '♠'],
	redUntilIndex: 26,
	Joker: 52,

	value: [-1,-1,-1,-1,-1],
	selected_index: -1,
};
const Field = {
	FreeSpace: Deck.size,
	clicked_index: -1,
};

function get_text(card_index) {
	if (card_index < 0 || card_index > Deck.size) return '';
	else if (card_index == Deck.Joker) return 'Joker';
	else if (card_index == Field.FreeSpace) return 'free\nspace';
	else return Deck.numbers[card_index % Deck.numbers.length] + '\n' +
		Deck.suits[card_index / Deck.numbers.length >> 0];
}

const State = {
	clickable: false,
	is_dark: false,
	counter: 0,
	history_size: -1,
};


/**
 * This callback is displayed as part of the Requester class.
 * @callback forEachChild
 * @param {Element} child
 * @param {number} index
 */
/**
 * @param {HTMLElement} element 
 * @param {forEachChild} block 
 */
function forEachChild(element, block) {
	const children = element.children;
	for (let index = 0; index < children.length; index++)
		block(children[index], index);
}


function initRender(event) {
	const { field_data } = event.detail.args;


	const add_cell_text = (cell, value, ...classes) => {
		const cell_text = document.createElement('div');
		cell_text.textContent = value;
		cell_text.classList.add(...classes);
		cell.appendChild(cell_text);
	};

	const field = document.getElementById('touche-field');
	field_data.forEach((value, index) => {
		const cell = document.createElement('div');
		const text = get_text(value);
		if (text.length > 0) cell.classList.add('cell', 'light-bg');

		if (value == Field.FreeSpace) add_cell_text(cell, text, 'cell-free-text', 'light-text');
		else if (text.length > 0) {
			const color_class = value < Deck.redUntilIndex ? 'red-text' : 'light-text';
			add_cell_text(cell, text, 'cell-card-text', color_class);
		}

		if (text.length > 0) cell.onclick = () => {
			if (State.clickable || Deck.selected_index == 5) {
				Field.clicked_index = index;
				Streamlit.setComponentValue({ cell_index: index, card_index: Deck.selected_index, counter: State.counter++ });
			}
		}

		field.appendChild(cell);
	});


	const deck = document.getElementById('deck');
	const card_crown_click = click_index => () => {
		if (Deck.selected_index == 5) deck.children[5].classList.remove('selected-crown');
		else if (Deck.selected_index != -1)
			forEachChild(deck.children[Deck.selected_index], card => card.classList.remove('selected-card'));
		if (click_index != Deck.selected_index) {
			if (click_index == 5) deck.children[5].classList.add('selected-crown');
			else forEachChild(deck.children[click_index], card => card.classList.add('selected-card'));
		}
		Deck.selected_index = click_index != Deck.selected_index ? click_index : -1;
	}
	forEachChild(deck, (card_crown, index) => card_crown.onclick = card_crown_click(index));


	setTimeout(() => {
		const { width, height } = document.body.getBoundingClientRect();
		Streamlit.setFrameHeight(height);
	}, 0);
}

function updateRender(event) {
	const { used_cells, user_color, history_size, cards, clickable, is_dark } = event.detail.args;


	const field = document.getElementById('touche-field');
	forEachChild(field, (cell, index) => {
		const used_cell = used_cells[index];
		var found_dot = undefined;
		forEachChild(cell, child => { if (child.tagName == 'SPAN') found_dot = child; });

		if (used_cell) {
			const dot = found_dot ? found_dot : document.createElement('span');
			dot.style.backgroundColor = user_color[used_cell.user_id];
			dot.className = '';
			let dot_class = 'dot';
			switch (used_cell.type) {
				case 'sf': dot_class = 'semi-final-dot'; break;
				case 'f': dot_class = 'final-dot'; break;
			}
			dot.classList.add(dot_class);
			if (!found_dot) cell.appendChild(dot);
		}
		else if (found_dot) found_dot.remove();
	});

	if (State.history_size == history_size && Field.clicked_index != -1) {
		const invalid_cell = field.children[Field.clicked_index];
		invalid_cell.classList.add('invalid-cell');
		setTimeout(() => invalid_cell.classList.remove('invalid-cell'), 1000);
	}
	else State.history_size = history_size;
	Field.clicked_index = -1;


	const deck = document.getElementById('deck');
	const update_card = (value, index) => {
		const card_holder = deck.children[index];

		forEachChild(card_holder, card => {		//There should be exactly o1e card, or 0 at the beggining
			card.classList.remove('selected-card');
			card.classList.add('played-card');
			setTimeout(() => card.remove(), 400);
		});

		const new_card = document.createElement('div');
		new_card.classList.add('card');
		['card-text', 'card-text-rotated'].forEach((text_class) => {
			const text = document.createElement('div');
			text.textContent = get_text(value);
			text.classList.add(text_class, value < Deck.redUntilIndex ? 'red-text' : 'black-text');
			new_card.appendChild(text);
		});
		card_holder.appendChild(new_card);

		if (Deck.selected_index == index) Deck.selected_index = -1;
	}
	for (let index = 0; index < 5; index++)
		if (Deck.value[index] != cards[index]) {
			Deck.value[index] = cards[index];
			update_card(cards[index] & 0xff, index);
		}


	State.clickable = clickable;

	if (State.is_dark != is_dark) {
		State.is_dark = is_dark;

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
	}

}

function onRender(event) {
	if (!window.rendered) {
		initRender(event);
		window.rendered = true;
	}
	updateRender(event);
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
Streamlit.setComponentReady();
Streamlit.setFrameHeight(-1);
