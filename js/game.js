class Game {
  constructor(canvas) {
    this.width = canvas.width;
    this.height = canvas.height;

    this.render = canvas.getContext('2d');

    this.entities = {};
    this.stars = new Stars(this.width, this.height, 4);
  }

  addEntity(entity) {
    if (entity.type === 'Spaceship') {
      this.player = entity;
    }
    this.entities[entity.entity] = entity;
  }

  removeEntity(entity) {
    delete this.entities[entity.entity];
  }

  update() {
    // Update the background
    this.stars.generate(this.width, this.height);
  }

  updateEntity(entity) {
    // Follow the player
    if (entity.entity === this.player.entity) {
      this.stars.offset(entity.pos[0], entity.pos[1]);
      this.entities[entity.entity].pos = entity.pos;
    } else {
      // Set the entity's new position
      this.entities[entity.entity].pos[0] = entity.pos[0] - this.player.pos[0];
      this.entities[entity.entity].pos[1] = entity.pos[1] - this.player.pos[1];
    }
  }

  draw() {
    // Draw the background
    this.drawSpace();
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
