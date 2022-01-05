import Card from './cards';

interface Count {
  type: Card;
  amount: number;
}

const cardCount: Count[] = [
  {
    type: Card.archer,
    amount: 4,
  },
  {
    type: Card.priest,
    amount: 2,
  },
  {
    type: Card.sword,
    amount: 2,
  },
  {
    type: Card.shield,
    amount: 2,
  },
  {
    type: Card.trebuchet,
    amount: 2,
  },
  {
    type: Card.mule,
    amount: 1,
  },
  {
    type: Card.joker,
    amount: 1,
  },
  {
    type: Card.crown,
    amount: 1,
  }
];

const deck = [

]
