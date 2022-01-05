import * as cardType from './cardType';
import createPlayer from './createPlayer';
import * as hand from './hand';
import UUID from './uuid';

export * from './cardType';
export * from './hand';
export {
  createPlayer,
  UUID
};

const utilities = {
  ...cardType,
  createPlayer,
  ...hand,
  UUID,
};

export default utilities;
