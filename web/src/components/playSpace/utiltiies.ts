export const getBackgroundColor = (isDragging: boolean, isOver: boolean): string => {
  if (isDragging) {
    return '#646335';
  }
  if (isOver) {
    return '#35643c';
  }
  return '#35654d';
}
