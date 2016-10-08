class Entity {
  constructor(x, y) {
    this.pos = [ x, y ];
  }

  static draw(render, entity) {
    render.fillStyle = 'white';
    const pos = norm(entity.pos[0], entity.pos[1]);
    render.fillRect(pos.x, pos.y, 150, 150);
  }
}
