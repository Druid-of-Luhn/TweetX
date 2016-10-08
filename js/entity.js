class Entity {
  static draw(render, entity) {
    render.fillStyle = 'white';
    render.save();
    // Rotate the sprite
    if (entity.hasOwnProperty('direction')) {
      render.rotate(entity.direction);
    }
    // Draw the sprite
    if (entity.type === 'Spaceship') {
      // Centre the player
      const pos = norm(0, 0);
      render.drawImage(document.images[0], pos.x, pos.y, entity.width, entity.height);
    } else {
      // Place the entity
      const pos = norm(entity.pos[0], entity.pos[1]);
      if (entity.type === 'Dolphin') {
        // Draw a dolphin
        render.drawImage(document.images[1], pos.x, pos.y, entity.width, entity.height);
      } else if (entity.type === 'Planet') {
        // Draw a planet
        render.beginPath();
        render.arc(pos.x, pos.y, entity.width, 0, 2 * Math.PI, true);
        render.closePath();
        render.fill();
      } else {
        // Draw an unknown entity
        render.fillRect(pos.x, pos.y, entity.width, entity.height);
      }
    }
    render.restore();
  }
}
