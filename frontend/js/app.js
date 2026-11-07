const dassItems = [
  "I found it hard to wind down.", "I was aware of dryness of my mouth.", "I could not seem to experience any positive feeling at all.", "I experienced breathing difficulty.", "I found it difficult to work up the initiative to do things.", "I tended to over-react to situations.", "I experienced trembling.", "I felt that I was using a lot of nervous energy.", "I was worried about situations in which I might panic and make a fool of myself.", "I felt that I had nothing to look forward to.", "I found myself getting agitated.", "I found it difficult to relax.", "I felt down-hearted and blue.", "I was intolerant of anything that kept me from getting on with what I was doing.", "I felt I was close to panic.", "I was unable to become enthusiastic about anything.", "I felt I was not worth much as a person.", "I felt that I was rather touchy.", "I was aware of the action of my heart in the absence of physical exertion.", "I felt scared without any good reason.", "I felt that life was meaningless."
];

const ipipItems = [
  "Am the life of the party.", "Feel little concern for others.", "Am always prepared.", "Get stressed out easily.", "Have a rich vocabulary.", "Don't talk a lot.", "Am interested in people.", "Leave my belongings around.", "Am relaxed most of the time.", "Have difficulty understanding abstract ideas.", "Feel comfortable around people.", "Insult people.", "Pay attention to details.", "Worry about things.", "Have a vivid imagination.", "Keep in the background.", "Sympathize with others' feelings.", "Make a mess of things.", "Seldom feel blue.", "Am not interested in abstract ideas.", "Start conversations.", "Am not interested in other people's problems.", "Get chores done right away.", "Am easily disturbed.", "Have excellent ideas.", "Have little to say.", "Have a soft heart.", "Often forget to put things back in their proper place.", "Get upset easily.", "Do not have a good imagination.", "Talk to a lot of different people at parties.", "Am not really interested in others.", "Like order.", "Change my mood a lot.", "Am quick to understand things.", "Don't like to draw attention to myself.", "Take time out for others.", "Shirk my duties.", "Have frequent mood swings.", "Use difficult words.", "Don't mind being the center of attention.", "Feel others' emotions.", "Follow a schedule.", "Get irritated easily.", "Spend time reflecting on things.", "Am quiet around strangers.", "Make people feel at ease.", "Am exacting in my work.", "Often feel blue.", "Am full of ideas."
];

const mbtiItems = [
  "I feel energized after spending time with a lively group.", "I usually start conversations with new people.", "I prefer sharing ideas aloud rather than thinking silently.", "I look forward to meeting several people at social events.",
  "I trust practical experience when making sense of a situation.", "I prefer clear facts over possibilities that are hard to verify.", "I notice concrete details before forming a big-picture impression.", "I like instructions that explain exactly what to do.",
  "I make important decisions by weighing evidence and consistency.", "I would rather hear an honest correction than a comforting answer.", "I naturally look for flaws in an argument.", "I try to separate a decision from my personal feelings.",
  "I like having a clear plan before I begin.", "I feel comfortable making decisions early.", "I prefer routines that help me stay organised.", "I like finishing one commitment before starting another."
];

const enneagramItems = [
  "I want to do what is right and improve what I can.", "I notice quickly when something feels inconsistent with my values.",
  "I feel most fulfilled when I can be helpful to someone.", "I often put another person's needs before my own.",
  "Achievement and visible progress motivate me strongly.", "I adapt how I present myself to reach an important goal.",
  "I want my life to feel distinct, meaningful, and authentic.", "I spend time understanding my emotions and identity.",
  "I need time alone to understand a subject deeply.", "I protect my energy and knowledge carefully.",
  "I pay close attention to risks and what could go wrong.", "I value reliable people, plans, and support systems.",
  "I enjoy keeping several exciting possibilities open.", "I look for the positive angle when life feels heavy.",
  "I naturally take charge when a situation needs direction.", "I speak directly when I believe something is important.",
  "I work hard to keep peace in the groups I belong to.", "I can see several sides of a disagreement."
];

const socialEnergyItems = [
  "I feel refreshed after a lively conversation.", "I need quiet time to feel like myself again.",
  "I enjoy being the first person to introduce myself.", "I prefer one deep conversation to a crowded gathering.",
  "I seek out new social experiences.", "I think best when I have space and little noise.",
  "I enjoy keeping in touch with many people.", "I am selective about who I spend a lot of time with.",
  "I often process my thoughts by talking them through.", "I usually process my thoughts privately first.",
  "A busy social calendar feels energising to me.", "A calm, open calendar feels restorative to me."
];

let dassChart;
let personalityChart;

const scaleLabels = {
  dass: ["Did not apply", "Applied some of the time", "Applied a good part of the time", "Applied most of the time"],
  personality: ["Very inaccurate", "Moderately inaccurate", "Neither accurate nor inaccurate", "Moderately accurate", "Very accurate"],
  mbti: ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],
  enneagram: ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],
  "social-energy": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
};

function renderQuestions(containerId, items, minimum, maximum, group) {
  const container = document.getElementById(containerId);
  container.replaceChildren();
  items.forEach((item, index) => {
    const question = document.createElement("div");
    question.className = "question reveal";
    question.dataset.group = group;
    question.dataset.index = String(index);
    question.dataset.motion = String(index % 6);
    question.id = `${group}-question-${index}`;

    const label = document.createElement("div");
    label.className = "question-text";
    label.textContent = `${index + 1}. ${item}`;

    const rating = document.createElement("div");
    rating.className = "rating";
    for (let value = minimum; value <= maximum; value += 1) {
      const option = document.createElement("label");
      const input = document.createElement("input");
      input.type = "radio";
      input.name = `${group}-${index}`;
      input.value = String(value);
      input.setAttribute("aria-label", `${item}: ${value}`);
      input.addEventListener("change", () => moveToNextUnanswered(group, items.length, index + 1));
      option.append(input, document.createTextNode(scaleLabels[group][value - minimum]));
      rating.append(option);
    }
    question.append(label, rating);
    container.append(question);
  });
}

function unansweredIndex(group, count, start = 0) {
  const order = Array.from({ length: count }, (_, index) => (start + index) % count);
  return order.find((index) => !document.querySelector(`input[name="${group}-${index}"]:checked`)) ?? -1;
}

function focusQuestion(group, index) {
  if (index < 0) return;
  const question = document.getElementById(`${group}-question-${index}`);
  if (!question) return;
  question.classList.remove("needs-answer");
  requestAnimationFrame(() => {
    question.scrollIntoView({ behavior: "smooth", block: "center" });
    question.classList.add("needs-answer");
  });
  window.setTimeout(() => question.classList.remove("needs-answer"), 2800);
}

function moveToNextUnanswered(group, count, start) {
  focusQuestion(group, unansweredIndex(group, count, start));
}

function getAnswers(group, count) {
  const missing = unansweredIndex(group, count);
  if (missing !== -1) {
    const error = new Error(`Please answer question ${missing + 1} before continuing.`);
    error.questionIndex = missing;
    throw error;
  }
  return Array.from({ length: count }, (_, index) => Number(document.querySelector(`input[name="${group}-${index}"]:checked`).value));
}

async function requestJson(url, answers) {
  const response = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ answers }) });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "The request could not be completed.");
  return payload;
}

function showError(targetId, error, group) {
  const target = document.getElementById(targetId);
  target.replaceChildren();
  const message = document.createElement("p");
  message.className = "error";
  message.textContent = error.message;
  target.append(message);
  if (Number.isInteger(error.questionIndex)) focusQuestion(group, error.questionIndex);
}

function makeResultCard(targetId, headingText) {
  const target = document.getElementById(targetId);
  target.replaceChildren();
  const card = document.createElement("article");
  card.className = "result-card";
  const heading = document.createElement("h3");
  heading.textContent = headingText;
  card.append(heading);
  target.append(card);
  return { target, card };
}

function addBenchmark(item, percentage, label = "Relative position") {
  const meter = document.createElement("div");
  meter.className = "benchmark";
  meter.innerHTML = `<div class="benchmark-label"><span>${label}</span><span>${Math.round(percentage)}%</span></div><div class="mini-meter"><span style="width:${Math.max(0, Math.min(100, percentage))}%"></span></div>`;
  item.append(meter);
}

function renderDass(result) {
  const { card } = makeResultCard("dass-result", "Your DASS-21 screening summary");
  document.getElementById("dass-chart").parentElement.classList.add("has-result");
  const grid = document.createElement("div");
  grid.className = "result-grid";
  const labels = ["depression", "anxiety", "stress"];
  labels.forEach((label) => {
    const score = document.createElement("div");
    score.className = "score";
    score.innerHTML = `<span>${label}</span><b>${result.scores[label].score}</b><span>${result.scores[label].severity}</span>`;
    addBenchmark(score, result.scores[label].score / 42 * 100, "Screening range");
    grid.append(score);
  });
  card.append(grid);
  if (labels.every((label) => result.scores[label].score === 0)) {
    const emptyNote = document.createElement("p");
    emptyNote.className = "result-note";
    emptyNote.textContent = "All three screening scores are 0 because each response was marked ‘Did not apply’.";
    card.append(emptyNote);
  }
  dassChart?.destroy();
  dassChart = new Chart(document.getElementById("dass-chart"), {
    type: "bar",
    data: { labels: labels.map((label) => label[0].toUpperCase() + label.slice(1)), datasets: [{ label: "Score", data: labels.map((label) => result.scores[label].score), backgroundColor: ["#ffffff", "#bdbdbd", "#ffffff"], borderRadius: 8 }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: "#ffffff" } } }, scales: { x: { ticks: { color: "#ffffff" }, grid: { color: "rgba(255,255,255,.12)" } }, y: { beginAtZero: true, suggestedMax: 42, ticks: { color: "#ffffff" }, grid: { color: "rgba(255,255,255,.12)" } } } }
  });
}

function renderPersonality(result) {
  const { card } = makeResultCard("personality-result", "Your Big Five profile");
  document.getElementById("personality-chart").parentElement.classList.add("has-result");
  const grid = document.createElement("div");
  grid.className = "result-grid";
  Object.entries(result.traits).forEach(([trait, score]) => {
    const item = document.createElement("div");
    item.className = "score";
    item.innerHTML = `<span>${trait}</span><b>${score.average} / 5</b><span>Total ${score.total} / 50</span>`;
    addBenchmark(item, score.average / 5 * 100, "Trait range");
    grid.append(item);
  });
  card.append(grid);
  personalityChart?.destroy();
  personalityChart = new Chart(document.getElementById("personality-chart"), {
    type: "radar",
    data: { labels: Object.keys(result.traits), datasets: [{ label: "Average trait score", data: Object.values(result.traits).map((score) => score.average), backgroundColor: "rgba(255, 255, 255, .18)", borderColor: "#ffffff", pointBackgroundColor: "#ffffff" }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: "#ffffff" } } }, scales: { r: { min: 0, max: 5, ticks: { stepSize: 1, color: "#ffffff" }, grid: { color: "rgba(255,255,255,.2)" }, angleLines: { color: "rgba(255,255,255,.2)" }, pointLabels: { color: "#ffffff" } } } }
  });
}

function renderMbti(result) {
  const { card } = makeResultCard("mbti-result", `Your preference pattern: ${result.type}`);
  const grid = document.createElement("div");
  grid.className = "result-grid";
  result.dimensions.forEach((dimension) => {
    const item = document.createElement("div");
    item.className = "score";
    item.innerHTML = `<span>${dimension.left} / ${dimension.right}</span><b>${dimension.left_score > dimension.right_score ? dimension.left : dimension.right}</b><span>${dimension.left_score} vs ${dimension.right_score}</span>`;
    addBenchmark(item, Math.max(dimension.left_score, dimension.right_score) / 20 * 100, "Preference strength");
    grid.append(item);
  });
  card.append(grid);
}

function renderEnneagram(result) {
  const { card } = makeResultCard("enneagram-result", `Your leading reflection: Style ${result.leading_style}`);
  const grid = document.createElement("div");
  grid.className = "result-grid";
  result.styles.slice(0, 3).forEach((style) => {
    const item = document.createElement("div");
    item.className = "score";
    item.innerHTML = `<span>Style ${style.number}</span><b>${style.score} / 10</b><span>Reflection ranking</span>`;
    addBenchmark(item, style.score / 10 * 100, "Reflection range");
    grid.append(item);
  });
  card.append(grid);
}

function renderSocialEnergy(result) {
  const { card } = makeResultCard("social-energy-result", result.style);
  const grid = document.createElement("div");
  grid.className = "result-grid";
  Object.entries(result.scores).forEach(([label, score]) => {
    const item = document.createElement("div");
    item.className = "score";
    item.innerHTML = `<span>${label}</span><b>${score} / 30</b><span>Reflection score</span>`;
    addBenchmark(item, score / 30 * 100, "Reflection range");
    grid.append(item);
  });
  card.append(grid);
}

function bindForm(formId, group, count, url, render, resultId) {
  document.getElementById(formId).addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      render(await requestJson(url, getAnswers(group, count)));
    } catch (error) {
      showError(resultId, error, group);
    }
  });
}

function activatePanel(panelId) {
  document.querySelectorAll(".panel").forEach((item) => item.classList.remove("active"));
  document.getElementById(panelId)?.classList.add("active");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function openOverlay(id) {
  const overlay = document.getElementById(id);
  overlay.hidden = false;
  overlay.style.display = "flex";
  document.body.classList.add("overlay-open");
}

function closeOverlay(id) {
  const overlay = document.getElementById(id);
  overlay.hidden = true;
  overlay.style.display = "";
  if (!document.querySelector(".overlay:not([hidden])")) document.body.classList.remove("overlay-open");
}

function applyTheme(theme) {
  document.body.dataset.theme = theme;
  document.documentElement.style.setProperty("--tunnel-bg", theme === "light" ? "#f7f7f7" : "#000000");
  document.getElementById("theme-toggle")?.replaceChildren(document.createTextNode(theme === "light" ? "Switch to black theme" : "Switch to white theme"));
}

function startRevealObserver() {
  const observer = new IntersectionObserver((entries) => entries.forEach((entry) => entry.isIntersecting && entry.target.classList.add("visible")), { threshold: .08 });
  document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));
}

document.getElementById("enter-matlas").addEventListener("click", () => {
  const landing = document.getElementById("landing");
  landing.classList.add("leaving");
  window.setTimeout(() => {
    landing.hidden = true;
    document.getElementById("app").hidden = false;
    startRevealObserver();
    window.scrollTo(0, 0);
    openOverlay("test-picker");
  }, 560);
});

document.querySelectorAll("[data-open-overlay]").forEach((button) => button.addEventListener("click", () => { openOverlay(button.dataset.openOverlay); document.querySelector(".safety-menu").removeAttribute("open"); }));
document.querySelectorAll("[data-close-overlay]").forEach((button) => button.addEventListener("click", () => closeOverlay(button.dataset.closeOverlay)));
document.querySelectorAll("[data-choose-test]").forEach((button) => button.addEventListener("click", () => { activatePanel(button.dataset.chooseTest); closeOverlay("test-picker"); document.querySelector(".safety-menu")?.removeAttribute("open"); }));
document.getElementById("theme-toggle")?.addEventListener("click", () => applyTheme(document.body.dataset.theme === "light" ? "dark" : "light"));
document.querySelectorAll("[data-wordmark]").forEach((wordmark) => wordmark.addEventListener("mouseenter", () => { wordmark.classList.remove("wordmark-replay"); requestAnimationFrame(() => wordmark.classList.add("wordmark-replay")); }));

let scrollFrame;
window.addEventListener("scroll", () => {
  if (scrollFrame) return;
  scrollFrame = requestAnimationFrame(() => {
    const center = window.innerHeight / 2;
    document.querySelectorAll(".reveal.visible").forEach((element) => {
      const distance = (element.getBoundingClientRect().top + element.offsetHeight / 2 - center) / Math.max(1, window.innerHeight);
      element.style.setProperty("--scroll-shift", `${Math.max(-7, Math.min(7, distance * -12))}px`);
      element.style.setProperty("--scroll-rotate", `${Math.max(-.7, Math.min(.7, distance * -.9))}deg`);
    });
    scrollFrame = null;
  });
}, { passive: true });

document.querySelectorAll("h2, .eyebrow, .question-text, .wiki-link").forEach((element) => {
  if (element.children.length > 0) return;
  const text = element.textContent;
  element.replaceChildren(...Array.from(text).map((character) => {
    const letter = document.createElement("span");
    letter.className = "glow-letter";
    letter.textContent = character === " " ? "\u00a0" : character;
    return letter;
  }));
});
applyTheme("dark");
renderQuestions("dass-questions", dassItems, 0, 3, "dass");
renderQuestions("personality-questions", ipipItems, 1, 5, "personality");
renderQuestions("mbti-questions", mbtiItems, 1, 5, "mbti");
renderQuestions("enneagram-questions", enneagramItems, 1, 5, "enneagram");
renderQuestions("social-energy-questions", socialEnergyItems, 1, 5, "social-energy");
bindForm("dass-form", "dass", dassItems.length, "/api/score/dass21", renderDass, "dass-result");
bindForm("personality-form", "personality", ipipItems.length, "/api/score/personality", renderPersonality, "personality-result");
bindForm("mbti-form", "mbti", mbtiItems.length, "/api/score/mbti", renderMbti, "mbti-result");
bindForm("enneagram-form", "enneagram", enneagramItems.length, "/api/score/enneagram", renderEnneagram, "enneagram-result");
bindForm("social-energy-form", "social-energy", socialEnergyItems.length, "/api/score/social-energy", renderSocialEnergy, "social-energy-result");
