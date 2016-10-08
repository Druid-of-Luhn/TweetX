class Entity {
  constructor(x, y, width, height) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
  }

  draw(render) {
    render.fillStyle = 'white';
    const pos = norm(this.x, this.y);
    render.fillRect(pos.x, pos.y, this.width, this.height);
  }
}
