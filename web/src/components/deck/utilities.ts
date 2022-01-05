import { CSSProperties } from 'react'
import { CARD_SIZES } from '../../constants'

export const getStyles = (hasDealt: boolean): CSSProperties => {
  if (hasDealt) {
    return {
      left: '75%',
      right: 0,
      top: 0,
    }
  }
  return {
    left: -CARD_SIZES.DECK.WIDTH / 4,
    top: window.innerHeight / 3,
  }
}
