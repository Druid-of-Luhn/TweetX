class Game {
  constructor(canvas) {
    this.width = canvas.width;
    this.height = canvas.height;

    this.render = canvas.getContext('2d');

    this.player = new Entity(0, 0, 200, 150);
    this.entities = [];
    this.stars = new Stars(this.width, this.height, 4);
  }

  setAnchor(x, y) {
    this.entities.forEach((e) => {
      e.x -= x;
      e.y -= y;
    });
    this.stars.offset(x, y);
  }

  setEntities(entities) {
    this.entities = entities.map((e) => {
      return new Entity(e.x, e.y, e.w, e.h);
    });
  }

  update() {
    // Update the background
    this.stars.generate(this.width, this.height);
  }

  draw() {
    // Draw the background
    this.drawSpace();
    // Draw the player
    this.player.draw(this.render);
    // Draw all other entities
    this.entities.forEach((e) => {
      e.draw(this.render);
    });
  }

  drawSpace() {
    // Draw the background in black
    this.render.fillStyle = 'black';
    this.render.fillRect(0, 0, this.width, this.height);
    // Draw the stars
    this.stars.draw(this.render);
  }
}
