class Game {
  constructor(canvas) {
    this.width = canvas.width;
    this.height = canvas.height;

    this.render = canvas.getContext('2d');

    this.player = new Entity(0, 0);
    this.entities = {};
    this.stars = new Stars(this.width, this.height, 4);
  }

  setAnchor(x, y) {
    this.entities.forEach((e) => {
      e.x -= x;
      e.y -= y;
    });
    this.stars.offset(x, y);
  }

  addEntity(entity) {
    this.entities[entity.entity] = entity;
  }

  removeEntity(entity) {
    delete this.entities[entity.entity];
  }

  update() {
    // Update the background
    this.stars.generate(this.width, this.height);
  }

  draw() {
    // Draw the background
    this.drawSpace();
    // Draw the player
    Entity.draw(this.render, this.player);
    // Draw all other entities
    for (const id in this.entities) {
      Entity.draw(this.render, this.entities[id]);
    }
  }

  drawSpace() {
    // Draw the background in black
    this.render.fillStyle = 'black';
    this.render.fillRect(0, 0, this.width, this.height);
    // Draw the stars
    this.stars.draw(this.render);
  }
}
