delete temp1;

queryObjects(WebSocket);

let snapshots = [];
temp1.addEventListener("message", function (event) {
  let data = "[" + event.data.replace(/\x1E/g, ",");
  data = JSON.parse(data.substring(0, data.length - 1) + "]");
  for (i = 0; i < data.length; i++) {
    if (data[i].target === "QuoteSnapshot") {
      snapshots.push(data[i]);
    }
  }
});
let updates = [];
temp1.addEventListener("message", function (event) {
  let data = "[" + event.data.replace(/\x1E/g, ",");
  data = JSON.parse(data.substring(0, data.length - 1) + "]");
  for (i = 0; i < data.length; i++) {
    if (data[i].target === "QuoteUpdate") {
      updates.push(data[i]);
    }
  }
});