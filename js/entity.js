class Entity {
  static draw(render, entity) {
    render.save();
    // Rotate the sprite
    if (entity.hasOwnProperty('direction')) {
      render.rotate(entity.direction);
    }
    // Draw the sprite
    if (entity.type === 'Spaceship') {
      // Centre the player
      const pos = norm(0, 0);
      render.drawImage(document.images[0], pos.x, pos.y);
    } else {
      // Place the entity
      const pos = norm(entity.pos[0], entity.pos[1]);
      // Draw a dolphin
      if (entity.type === 'Dolphin') {
        render.drawImage(document.images[1], pos.x, pos.y);
      } else {
        // Draw an unknown entity
        render.fillStyle = 'white';
        render.fillRect(pos.x, pos.y, 100, 80);
      }
    }
    render.restore();
  }
}
