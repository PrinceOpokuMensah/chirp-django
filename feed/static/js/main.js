// Like/unlike without a page reload
document.querySelectorAll(".like-form").forEach((form) => {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.body.dataset.csrf,
          "X-Requested-With": "XMLHttpRequest",
        },
      });
      if (!res.ok) throw new Error();
      const data = await res.json();
      const btn = form.querySelector(".like");
      btn.classList.toggle("liked", data.liked);
      form.querySelector(".heart").textContent = data.liked ? "♥" : "♡";
      form.querySelector(".count").textContent = data.count;
    } catch {
      form.submit(); // fall back to a normal request
    }
  });
});

// Confirm destructive actions
document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (e) => {
    if (!confirm(form.dataset.confirm)) e.preventDefault();
  });
});

setTimeout(() => document.querySelectorAll(".msg").forEach((m) => (m.style.display = "none")), 4000);
