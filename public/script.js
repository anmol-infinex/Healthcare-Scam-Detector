const suspiciousTerms = [
  "urgent",
  "verify",
  "password",
  "ssn",
  "social security",
  "bank",
  "claim",
  "refund",
  "medicare card",
  "medicaid",
  "insurance suspended",
  "click",
  "link",
  "gift card",
  "otp",
  "one time password",
  "account locked",
  "billing problem",
  "free test",
  "limited time",
  "confirm identity",
  "routing number",
  "credit card"
];

const healthcareTerms = [
  "medicare",
  "medicaid",
  "clinic",
  "hospital",
  "pharmacy",
  "insurance",
  "patient",
  "prescription",
  "appointment",
  "lab",
  "doctor"
];

const message = document.querySelector("#message");
const analyze = document.querySelector("#analyze");
const sample = document.querySelector("#sample");
const result = document.querySelector("#result");
const label = document.querySelector("#label");
const bar = document.querySelector("#bar");
const explanation = document.querySelector("#explanation");
const terms = document.querySelector("#terms");

function scoreText(text) {
  const lowered = text.toLowerCase();
  const hits = suspiciousTerms.filter((term) => lowered.includes(term));
  const healthcareHits = healthcareTerms.filter((term) => lowered.includes(term));
  const pressure = /\b(now|today|final notice|within \d+ minutes|immediately)\b/i.test(text) ? 1 : 0;
  const urlSignal = /(https?:\/\/|bit\.ly|tinyurl|click here)/i.test(text) ? 1 : 0;
  const score = Math.min(0.96, 0.12 + hits.length * 0.11 + healthcareHits.length * 0.025 + pressure * 0.14 + urlSignal * 0.14);
  return { score, hits };
}

function render() {
  const text = message.value.trim();
  if (!text) {
    result.className = "result idle";
    label.textContent = "No prediction yet";
    bar.style.width = "0%";
    explanation.textContent = "Paste a message to screen it for common healthcare scam and phishing signals.";
    terms.innerHTML = "";
    return;
  }

  const { score, hits } = scoreText(text);
  const isScam = score >= 0.48;
  result.className = `result ${isScam ? "scam" : "legit"}`;
  label.textContent = `${isScam ? "Scam / Phishing" : "Legitimate"} (${Math.round((isScam ? score : 1 - score) * 100)}% confidence)`;
  bar.style.width = `${Math.round(score * 100)}%`;
  bar.style.background = isScam ? "#b42318" : "#16703c";
  explanation.textContent = isScam
    ? "The message contains urgency, identity, payment, or link patterns often used in healthcare scams."
    : "The message looks closer to routine healthcare communication, but verify through official channels when unsure.";
  terms.innerHTML = hits.map((term) => `<span>${term}</span>`).join("");
}

analyze.addEventListener("click", render);
sample.addEventListener("click", () => {
  message.value = "Urgent Medicare refund approved. Click this link now to verify your SSN and bank account.";
  render();
});
