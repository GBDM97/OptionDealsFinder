delete temp1;

queryObjects(WebSocket);
let snaphshots = [];
temp1.addEventListener("message", function (event) {
  let data = "[" + event.data.replace(/\x1E/g, ",");
  data = JSON.parse(data.substring(0, data.length - 1) + "]");
  for (i = 0; i < data.length; i++) {
    if (data[i].target === "QuoteSnapshot") {
      snaphshots.push(data[i]);
    }
  }
});
let updates = [];
temp1.addEventListener("message", function (event) {
  let data = "[" + event.data.replace(/\x1E/g, ",");
  data = JSON.parse(data.substring(0, data.length - 1) + "]");
  for (i = 0; i < data.length; i++) {
    if (data[i].target === "QuoteUpdates") {
      updates.push(data[i]);
    }
  }
});