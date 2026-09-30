// Open every hidden answer before printing, so the printed page is complete.
window.addEventListener("beforeprint", function () {
  document.querySelectorAll("details").forEach(function (d) { d.open = true; });
});
// Mark each table that is wider than its frame. The styles then show a hint and keep the title in view.
function markWideTables() {
  document.querySelectorAll(".table-wrap").forEach(function (w) {
    w.classList.toggle("scrolls", w.scrollWidth > w.clientWidth + 1);
    w.style.setProperty("--wrap-width", w.clientWidth + "px");
  });
}
window.addEventListener("load", markWideTables);
window.addEventListener("resize", markWideTables);
