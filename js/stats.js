function updateRange(type, value) {
  const range = document.querySelector('.js-stats-' + type);
  if (range && value >= range.min && value <= range.max) {
    range.value = value;
    rangeGradient(range, 'red', 'white');
  }
}

function rangeGradient(range, fg, bg) {
  const percent = (range.value / (range.max - range.min)) * 100;
  range.setAttribute('style',
      `background-image: linear-gradient(90deg, ${fg} ${percent}%, ${bg} ${percent}%)`);
}
