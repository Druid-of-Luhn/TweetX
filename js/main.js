// Get the canvas and context to draw to
const canvas = document.querySelector('.js-canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const centre = {
  x: canvas.width / 2,
  y: canvas.height / 2
};

// Create the game
let game = new Game(canvas);
// Game loop
requestAnimationFrame(loop);

// Receive data on a websocket
const ws = new WebSocket('ws://localhost:17922');
ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  if (data.hasOwnProperty('added') && data.added) {
    // Set the player entity
    if (data.type === 'Spaceship') {
      game.player = data.entity;
    }
    // Add the new entity
    game.addEntity(data);
  }
  if (data.hasOwnProperty('pos')) {
    // Set the entity's postition
    game.updateEntity(data);
  }
};

function norm(x, y) {
  return {
    x: centre.x + x,
    y: centre.y + y
  };
}

// The main game loop
function loop() {
  game.update();
  game.draw();
  requestAnimationFrame(loop);
}
