(() => {
  const $ = (id) => document.getElementById(id);

  const stage = $("stage");
  const mainImg = $("mainImg");
  const info = document.querySelector(".info");
  const thumbList = $("thumbList");
  const dots = $("dots");
  const downloadBtn = $("downloadBtn");
  const fullBtn = $("fullBtn");
  const icoExpand = $("icoExpand");
  const icoShrink = $("icoShrink");

  let characters = [];
  let index = 0;
  let themeRequest = 0;
  let autoplayTimer = null;
  const AUTOPLAY_INTERVAL = 6000;

  function setTheme(imageUrl) {
    document.documentElement.style.setProperty("--ambient-image", `url("${imageUrl}")`);
    const request = ++themeRequest;
    const image = new Image();

    image.addEventListener("load", () => {
      if (request !== themeRequest) return;

      const canvas = document.createElement("canvas");
      canvas.width = 1;
      canvas.height = 1;
      const context = canvas.getContext("2d");
      if (!context) return;

      context.drawImage(image, 0, 0, 1, 1);
      const [red, green, blue] = context.getImageData(0, 0, 1, 1).data;
      const r = red / 255;
      const g = green / 255;
      const b = blue / 255;
      const max = Math.max(r, g, b);
      const min = Math.min(r, g, b);
      const delta = max - min;
      let hue = 0;

      if (delta) {
        if (max === r) hue = 60 * (((g - b) / delta) % 6);
        else if (max === g) hue = 60 * ((b - r) / delta + 2);
        else hue = 60 * ((r - g) / delta + 4);
      }

      hue = (hue + 360) % 360;
      document.documentElement.style.setProperty("--accent", `hsl(${hue} 72% 58%)`);
      document.documentElement.style.setProperty("--accent-soft", `hsl(${hue} 82% 76%)`);
    });

    image.src = imageUrl;
  }

  fetch("/api/characters")
    .then((r) => r.json())
    .then((data) => {
      characters = data;
      $("total").textContent = characters.length;
      buildThumbs();
      buildDots();
      show(0, true);
      startAutoplay();
    })
    .catch(() => {
      $("name").textContent = "Couldn’t load characters";
      $("bio").textContent = "Make sure the Python server is running, then refresh the page.";
    });

  function buildThumbs() {
    thumbList.innerHTML = "";
    characters.forEach((c, i) => {
      const btn = document.createElement("button");
      btn.className = "thumb";
      btn.setAttribute("role", "tab");
      btn.setAttribute("aria-label", c.name);
      btn.innerHTML = `<img src="${c.image}" alt="" loading="lazy" /><span>${c.name}</span>`;
      btn.addEventListener("click", () => show(i));
      thumbList.appendChild(btn);
    });
  }

  function buildDots() {
    dots.innerHTML = characters.map(() => "<span></span>").join("");
  }

  function centerActiveThumbnail() {
    const activeThumbnail = thumbList.children[index];
    if (!activeThumbnail) return;

    const listBounds = thumbList.getBoundingClientRect();
    const thumbnailBounds = activeThumbnail.getBoundingClientRect();
    const left = thumbList.scrollLeft
      + thumbnailBounds.left
      - listBounds.left
      - (thumbList.clientWidth - activeThumbnail.clientWidth) / 2;

    thumbList.scrollTo({ left, behavior: "smooth" });
  }

  function show(i, instant = false) {
    index = (i + characters.length) % characters.length;
    const c = characters[index];

    const apply = () => {
      setTheme(c.image);
      mainImg.src = c.image;
      mainImg.alt = `${c.name} from ${c.anime}`;
      $("name").textContent = c.name;
      $("series").textContent = c.anime;
      $("bio").textContent = c.bio;
      $("tags").innerHTML = c.tags.map((t) => `<li>${t}</li>`).join("");
      $("current").textContent = index + 1;
      downloadBtn.href = c.download;

      info.classList.remove("swap");
      void info.offsetWidth;
      info.classList.add("swap");

      mainImg.classList.remove("swap");
    };

    [...thumbList.children].forEach((el, n) => {
      el.classList.toggle("active", n === index);
      el.setAttribute("aria-selected", n === index);
    });
    [...dots.children].forEach((el, n) => el.classList.toggle("on", n === index));
    centerActiveThumbnail();

    if (instant) return apply();

    mainImg.classList.add("swap");
    setTimeout(apply, 220);
  }

  const next = () => show(index + 1);
  const prev = () => show(index - 1);

  function startAutoplay() {
    window.clearInterval(autoplayTimer);
    autoplayTimer = window.setInterval(next, AUTOPLAY_INTERVAL);
  }

  stage.addEventListener("pointerenter", () => window.clearInterval(autoplayTimer));
  stage.addEventListener("pointerleave", startAutoplay);

  document.querySelectorAll("[data-dir]").forEach((btn) =>
    btn.addEventListener("click", () => (Number(btn.dataset.dir) > 0 ? next() : prev()))
  );

  function isFull() {
    return document.fullscreenElement || document.webkitFullscreenElement;
  }

  fullBtn.addEventListener("click", () => {
    if (isFull()) {
      (document.exitFullscreen || document.webkitExitFullscreen).call(document);
    } else {
      (stage.requestFullscreen || stage.webkitRequestFullscreen).call(stage);
    }
  });

  function syncFullIcon() {
    const full = !!isFull();
    icoExpand.hidden = full;
    icoShrink.hidden = !full;
    fullBtn.setAttribute("aria-label", full ? "Exit full screen" : "Fill the screen");
  }
  document.addEventListener("fullscreenchange", syncFullIcon);
  document.addEventListener("webkitfullscreenchange", syncFullIcon);

  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") next();
    else if (e.key === "ArrowLeft") prev();
    else if (e.key.toLowerCase() === "f") fullBtn.click();
  });

  let startX = null;
  stage.addEventListener("touchstart", (e) => (startX = e.touches[0].clientX), { passive: true });
  stage.addEventListener("touchend", (e) => {
    if (startX === null) return;
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) dx < 0 ? next() : prev();
    startX = null;
  });
})();