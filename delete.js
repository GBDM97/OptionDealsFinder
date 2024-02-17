(() => {
  const elements = Array.from(
    document.body.querySelectorAll('[arialabel="Remover ativo"]')
  ).map((e) => e.shadowRoot.querySelector('[type="button"]'));
  elements.forEach((e) => e.click());
})();
