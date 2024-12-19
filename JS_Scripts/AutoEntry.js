const lockQuantity = 2;

const gridElements = Array.from(
  document
    .querySelector("[caption='Grade de Cotações']")
    .querySelector("soma-table-body").children
);

const entryElements = gridElements.slice(
  gridElements.length - 2,
  gridElements.length
);

function sleep(milliseconds) {
  return new Promise(resolve => setTimeout(resolve, milliseconds));
}

function fillAndSendOrder(quantity) {
  sleep(10).then(() =>
    document.querySelector('[aria-label="A mercado"]').click()
  );
  sleep(10).then(() =>
    document.querySelector('[aria-label="Seleção do tipo da ordem"]').click()
  );
  sleep(200).then(() => {
    document.querySelector("[name=quantity]").value = quantity;
  });
  sleep(500).then(() =>
    document
      .querySelector('[aria-label="Revisar dados da boleta"]')
      .shadowRoot.querySelector('[type="button"]')
      .click()
  );
}

entryElements[1].lastChild
  .querySelector("[arialabel='Comprar']")
  .shadowRoot.querySelector("button")
  .click();

fillAndSendOrder(lockQuantity);

sleep(500).then(() => {
  entryElements[0].lastChild
    .querySelector("[arialabel='Vender']")
    .shadowRoot.querySelector("button")
    .click();
  fillAndSendOrder(lockQuantity);
});
