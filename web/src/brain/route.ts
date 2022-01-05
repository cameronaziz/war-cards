const needsChoice = (card: Cards.Card) => {
  const { rank } = card;
  switch (rank) {
    case '1':
    case '2':
    case '3':
    case '5':
    case '6':
      return true
    case '4':
    case '7':
    case '8':
    default:
      return false

  }
};

export default needsChoice;
