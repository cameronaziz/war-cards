const createPlayer = (id: string): Players.Player => ({
  id,
  isShielded: false,
  isDead: false,
});

export default createPlayer;
