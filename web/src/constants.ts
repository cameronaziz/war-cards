
export const BASE_IMAGE_SIZE = {
  WIDTH: 212,
  HEIGHT: 337,
};

export const CARD_SIZE: { [key: string]: Cards.Size } = {
  player: '0.5',
  deck: '0.75',
  opponent: '0.5',
};

export const CARD_SIZES = {
  PLAYER: {
    WIDTH: BASE_IMAGE_SIZE.WIDTH * parseFloat(CARD_SIZE.player),
    HEIGHT: BASE_IMAGE_SIZE.HEIGHT * parseFloat(CARD_SIZE.player),
  },
  DECK: {
    WIDTH: BASE_IMAGE_SIZE.WIDTH * parseFloat(CARD_SIZE.deck),
    HEIGHT: BASE_IMAGE_SIZE.HEIGHT * parseFloat(CARD_SIZE.deck),
  },
  OPPONENT: {
    WIDTH: BASE_IMAGE_SIZE.WIDTH * parseFloat(CARD_SIZE.opponent),
    HEIGHT: BASE_IMAGE_SIZE.HEIGHT * parseFloat(CARD_SIZE.opponent),
  },
}
