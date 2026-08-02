const message = document.querySelector("#message");
const analyze = document.querySelector("#analyze");
const sample = document.querySelector("#sample");
const result = document.querySelector("#result");
const statusText = document.querySelector(".status");
const label = document.querySelector("#label");
const bar = document.querySelector("#bar");
const explanation = document.querySelector("#explanation");
const terms = document.querySelector("#terms");

function setBusy(isBusy) {
  analyze.disabled = isBusy;
  analyze.textContent = isBusy ? "Analyzing..." : "Analyze";
}

function renderEmpty() {
  result.className = "result idle";
  statusText.textContent = "Waiting for message";
  label.textContent = "No prediction yet";
  bar.style.width = "0%";
  explanation.textContent = "Paste a message to screen it with the trained healthcare scam classifier.";
  terms.innerHTML = "";
}

function renderError(messageText) {
  result.className = "result scam";
  statusText.textContent = "Request failed";
  label.textContent = "Unable to analyze";
  bar.style.width = "0%";
  explanation.textContent = messageText;
  terms.innerHTML = "";
}

function renderPrediction(data) {
  const isScam = data.label === "scam";
  const confidence = Math.round(data.confidence * 100);
  const scamProbability = Math.round(data.scam_probability * 100);
  result.className = `result ${isScam ? "scam" : "legit"}`;
  statusText.textContent = `Scam probability: ${scamProbability}%`;
  label.textContent = `${data.display_label} (${confidence}% confidence)`;
  bar.style.width = `${scamProbability}%`;
  bar.style.background = isScam ? "#b42318" : "#16703c";
  explanation.textContent = data.explanation;
  terms.innerHTML = data.suspicious_terms.map((term) => `<span>${term}</span>`).join("");
}

async function render() {
  const text = message.value.trim();
  if (!text) {
    renderEmpty();
    return;
  }

  setBusy(true);
  statusText.textContent = "Calling model API";
  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Prediction service returned an error.");
    }
    renderPrediction(data);
  } catch (error) {
    renderError(error.message || "Prediction service is unavailable.");
  } finally {
    setBusy(false);
  }
}

analyze.addEventListener("click", render);
sample.addEventListener("click", () => {
  message.value = "Urgent Medicare refund approved. Click this link now to verify your SSN and bank account.";
  render();
});

renderEmpty();
