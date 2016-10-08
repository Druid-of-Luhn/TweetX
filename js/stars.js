class Stars {
  constructor(width, height, seed) {
    this.seed = seed;
    this.offX = 0;
    this.offY = 0;
    this.generate(width, height);
  }

  generate(width, height) {
    let stars = [];
    const scale = 0.1;
    const threshold = 0.9;
    // Set the seed
    noise.seed(this.seed);
    for (let x = 0; x < width; ++x) {
      for (let y = 0; y < height; ++y) {
        const posX = (x + this.offX) * scale;
        const posY = (y + this.offY) * scale;
        // Some pixels have stars on
        if (noise.simplex2(posX, posY) > threshold) {
          stars.push({
            x: x,
            y: y,
            // Stars have a random size
            size: 1.4,
          });
        }
      }
    }
    this.stars = stars;
  }

  offset(x, y) {
    this.offX = x;
    this.offY = y;
  }

  draw(context) {
    context.fillStyle = 'white';
    this.stars.forEach((star) => {
      context.fillRect(star.x, star.y, star.size, star.size);
    });
  }
}
