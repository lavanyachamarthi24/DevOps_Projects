const out = document.getElementById("out");

async function call(path) {
  out.textContent = `Calling ${path} ...`;
  try {
    const r = await fetch(path, { headers: { Accept: "application/json" } });
    const text = await r.text();
    out.textContent = `Status: ${r.status}\n\n${text}`;
  } catch (e) {
    out.textContent = `Error: ${e?.message || String(e)}`;
  }
}

document.getElementById("hello").addEventListener("click", () => call("/api/hello"));
document.getElementById("time").addEventListener("click", () => call("/api/time"));
document.getElementById("ready").addEventListener("click", () => call("/readyz"));

