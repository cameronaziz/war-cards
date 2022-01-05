import { atom } from 'recoil';

const UI_DEFAULT: State.UI = {
  hands: {},
  draggingCardId: null,
  dragState: 'default',
  playSpace: null,
  modalState: null,
}

const ui = atom({
  key: 'uiState',
  default: UI_DEFAULT,
});

export default ui;
