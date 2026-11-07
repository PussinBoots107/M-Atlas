(() => {
  const canvas = document.getElementById("tunnel-canvas");
  if (!canvas) return;
  const context = canvas.getContext("2d");
  if (!context) return;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const particles = Array.from({ length: reducedMotion ? 220 : 760 }, (_, index) => ({
    angle: (index / 760) * Math.PI * 2 + Math.random() * .5,
    radius: 24 + Math.random() * 180,
    z: 4 + Math.random() * 96,
    speed: .65 + Math.random() * 1.2,
    size: .45 + Math.random() * 1.7,
    drift: (Math.random() - .5) * .2,
  }));
  const pointer = { x: 0, y: 0, tx: 0, ty: 0, vx: 0, vy: 0 };
  let width = 0;
  let height = 0;
  let last = performance.now();

  function resize() {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
  }

  function readColor(name, fallback) {
    const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return value || fallback;
  }

  function frame(now) {
    const delta = Math.min((now - last) / 16.67, 3);
    last = now;
    pointer.x += (pointer.tx - pointer.x) * .105 * delta;
    pointer.y += (pointer.ty - pointer.y) * .105 * delta;
    pointer.vx *= .9;
    pointer.vy *= .9;
    context.fillStyle = readColor("--tunnel-bg", "#08090d");
    context.globalAlpha = .35;
    context.fillRect(0, 0, width, height);
    context.globalAlpha = 1;

    const nearColor = readColor("--tunnel-a", "#e9e9e9");
    const farColor = readColor("--tunnel-b", "#777777");
    const centerX = width / 2 + pointer.x * 72 + pointer.vx * 18;
    const centerY = height / 2 + pointer.y * 52 + pointer.vy * 18;
    const scale = Math.min(width, height) / 820;

    particles.forEach((particle) => {
      particle.z -= particle.speed * delta;
      particle.angle += (particle.drift * .003 + pointer.vx * .0009 - pointer.vy * .0005) * delta;
      if (particle.z < 1) {
        particle.z = 100;
        particle.radius = 24 + Math.random() * 180;
      }
      const depth = 1 - particle.z / 100;
      const perspective = (1 / particle.z) * 78 * scale;
      const x = centerX + Math.cos(particle.angle + pointer.x * .55 + pointer.vx * .03) * particle.radius * perspective;
      const y = centerY + Math.sin(particle.angle + pointer.y * .42 + pointer.vy * .03) * particle.radius * perspective;
      if (x < -20 || x > width + 20 || y < -20 || y > height + 20) return;
      const alpha = Math.min(.82, .08 + depth * .88);
      const size = Math.max(.45, particle.size * (.45 + depth * 2.2));
      context.globalAlpha = alpha;
      context.fillStyle = depth > .55 ? nearColor : farColor;
      context.fillRect(x, y, size, size);
    });
    context.globalAlpha = 1;
    requestAnimationFrame(frame);
  }

  window.addEventListener("resize", resize);
  window.addEventListener("pointermove", (event) => {
    const nextX = (event.clientX / Math.max(1, width) - .5) * 2;
    const nextY = (event.clientY / Math.max(1, height) - .5) * 2;
    pointer.vx += nextX - pointer.tx;
    pointer.vy += nextY - pointer.ty;
    pointer.tx = nextX;
    pointer.ty = nextY;
  }, { passive: true });
  resize();
  requestAnimationFrame(frame);
})();
