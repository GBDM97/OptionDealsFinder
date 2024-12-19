const lockQuantity = 2;
const slot = 0;

const gridElements = Array.from(
  document
    .querySelector("[caption='Grade de Cotações']")
    .querySelector("soma-table-body").children
);

const entryElements = gridElements.slice(slot, slot + 2);

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
  .querySelector("[arialabel='Vender']")
  .shadowRoot.querySelector("button")
  .click();

fillAndSendOrder(lockQuantity);

sleep(500).then(() => {
  entryElements[0].lastChild
    .querySelector("[arialabel='Comprar']")
    .shadowRoot.querySelector("button")
    .click();
  fillAndSendOrder(lockQuantity);
});

//the operation is exited for the current slot selected of the grid quotation, for example: 0 is for the first and second assets, following the correct order of the first beign early expiry and latter being the latter expiry
