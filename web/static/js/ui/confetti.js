const COLORS = ['#86dfc6', '#e9c283', '#8bcdea', '#cbb0e5', '#f3e7ca'];
const DURATION = 3200;

export function createConfetti(modal) {
  const canvas = document.getElementById('victory-confetti');
  const context = canvas.getContext('2d');
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0;
  let width = 0, height = 0;

  function resize() {
    if (canvas.hidden) return;
    width = window.innerWidth;
    height = window.innerHeight;
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
  }

  function stop() {
    cancelAnimationFrame(frame);
    frame = 0;
    modal.classList.remove('is-celebrating');
    canvas.hidden = true;
    canvas.width = canvas.height = 1;
  }

  function play() {
    stop();
    if (!context || motion.matches || document.hidden || modal.hidden) return;
    canvas.hidden = false;
    resize();
    modal.classList.add('is-celebrating');
    const count = width < 600 ? 64 : 112;
    const horizontalScale = Math.min(1, width / 900);
    const verticalScale = Math.min(1, Math.max(0.6, height / 850));
    const particles = Array.from({ length: count }, (_, index) => {
      const side = index % 2;
      return {
        origin: side ? 0.88 : 0.12,
        vx: (side ? -1 : 1) * (230 + Math.random() * 260) * horizontalScale,
        vy: -(470 + Math.random() * 300) * verticalScale,
        delay: Math.random() * 0.30,
        size: 4 + Math.random() * 4,
        spin: (Math.random() - 0.5) * 12,
        angle: Math.random() * Math.PI * 2,
        color: COLORS[index % COLORS.length],
        circle: index % 6 === 0,
      };
    });
    const started = performance.now();

    function draw(now) {
      const elapsed = now - started;
      if (elapsed >= DURATION || modal.hidden || motion.matches) return stop();
      context.clearRect(0, 0, width, height);
      const fade = Math.min(1, (DURATION - elapsed) / 700);
      particles.forEach(particle => {
        const t = elapsed / 1000 - particle.delay;
        if (t < 0) return;
        const x = width * particle.origin + particle.vx * (1 - Math.exp(-1.25 * t)) / 1.25;
        const y = height * 0.78 + particle.vy * t + 340 * verticalScale * t * t;
        if (y > height + 20 || x < -20 || x > width + 20) return;
        context.save();
        context.globalAlpha = Math.min(1, t / 0.1) * fade * 0.9;
        context.translate(x, y);
        context.rotate(particle.angle + particle.spin * t);
        context.fillStyle = particle.color;
        if (particle.circle) {
          context.beginPath();
          context.arc(0, 0, particle.size * 0.45, 0, Math.PI * 2);
          context.fill();
        } else {
          const tilt = Math.max(0.15, Math.abs(Math.cos(t * 8 + particle.angle)));
          context.fillRect(-particle.size / 2, -particle.size / 3, particle.size, particle.size * tilt * 0.65);
        }
        context.restore();
      });
      frame = requestAnimationFrame(draw);
    }
    frame = requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  motion.addEventListener('change', event => { if (event.matches) stop(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
  return { play, stop };
}
