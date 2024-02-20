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

async function waitForElm(selector) {
  return new Promise((resolve) => {
    if (document.querySelector(selector)) {
      return resolve(document.querySelector(selector));
    }

    const observer = new MutationObserver((mutations) => {
      if (document.querySelector(selector)) {
        observer.disconnect();
        resolve(document.querySelector(selector));
      }
    });

    // If you get "parameter 1 is not of type 'Node'" error, see https://stackoverflow.com/a/77855838/492336
    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
  });
}

await waitForElm('[placeholder="Novo ativo"]');
let e = document
  .querySelector('[placeholder="Novo ativo"]')
  .shadowRoot.querySelector('[placeholder="Novo ativo"]');
e.click();

let arr = [];
let changeable = true;

Object.keys(window).forEach((key) => {
  if (/^on/.test(key)) {
    window.addEventListener(key.slice(2), (event) => {
      if (changeable && arr.length < 12) {
        arr.push(event);
      }
    });
  }
});
