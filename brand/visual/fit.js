/* Fit display type to a fixed frame.
   Copy length changes the type size, never the layout, so a
   profile grid of mixed posts still lines up. */
(function () {
  document.querySelectorAll('[data-fit]').forEach(function (el) {
    var box = el.parentElement;
    var size = parseFloat(getComputedStyle(el).fontSize);
    var floor = parseFloat(el.dataset.floor || '34');
    var guard = 0;
    while (el.scrollHeight > box.clientHeight + 1 && size > floor && guard++ < 400) {
      size -= 1;
      el.style.fontSize = size + 'px';
    }
    el.dataset.fittedAt = size;
  });
  document.documentElement.setAttribute('data-ready', '1');
})();
