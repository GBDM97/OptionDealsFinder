function onIntersection(entries, observer) {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      observer.disconnect();
    }
  });
}

async function addAsset(ticker) {
  const observer = new IntersectionObserver(onIntersection);
  document.querySelector('[data-testid="icon-modal-stock"]').click();
  observer.observe(document.querySelector('[placeholder="Novo ativo"]'));
  let e = document.querySelector('[placeholder="Novo ativo"]');
  e.click();
  e.value = ticker;
  e = document.querySelector("[alt='Logo do ativo " + ticker + "']");
  observer.observe(e);
  e.click();
  document
    .querySelector('[arialabel="Salvar"]')
    .shadowRoot.querySelector('[type="button"]')
    .click();
}

addAsset("ZAMP3");
