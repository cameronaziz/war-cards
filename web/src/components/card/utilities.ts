import style from './style.module.scss';
const MAX_ROTATION = 4;

interface CardImageOptions {
  rank?: Cards.Rank;
  size?: Cards.Size;
  isFaceDown?: boolean;
  isPlayer: boolean;
}

const getCardSize = (size?: Cards.Size): string => {
  const ext = 'x.png';
  switch (size) {
    case '0.5':
      return `@05${ext}`;
    case '0.75':
      return `@075${ext}`;
    case '2':
      return `@2${ext}`;
    case '3':
      return `@3${ext}`;
    default:
      return '.png';
  }
}

export const cardImage = (options: CardImageOptions): string => {
  const { rank, isFaceDown, isPlayer, size } = options;
  const base = '/images/faces/';
  const ext = getCardSize(size);

  if (!rank) {
    return `/images/empty${ext}`;
  }

  if (isFaceDown || !isPlayer) {
    return `/images/back${ext}`;
  }

  switch (rank) {
    case '1': return `${base}1-archer${ext}`;
    case '2': return `${base}2-priest${ext}`;
    case '3': return `${base}3-swords${ext}`;
    case '4': return `${base}4-shield${ext}`;
    case '5': return `${base}5-trebuchet${ext}`;
    case '6': return `${base}6-mule${ext}`;
    case '7': return `${base}7-horse${ext}`;
    case '8': return `${base}8-crown${ext}`;
    default: return `/images/empty${ext}`;
  }
}

export const getTransform = (isRotated?: boolean, rotateAmount?: number): string | undefined => {
  if (!isRotated && !rotateAmount) {
    return undefined;
  };

  const rotate = rotateAmount ? rotateAmount : 0;
  const rotation = Math.random() - 0.5;
  const amount = rotation * MAX_ROTATION * 2
  const change = isRotated ? amount + rotate : rotate;
  return `rotate(${change}deg)`;
};

export const getContainerClassName = (isFlipping: boolean, isAbsolute?: boolean): string => {
  const base = isAbsolute ? style.containerAbsolute : style.container;
  const animation = isFlipping ? 'animate__animated animate__flip' : ''

  return `${base} ${animation}`
}
