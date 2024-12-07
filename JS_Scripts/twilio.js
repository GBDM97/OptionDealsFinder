var xhr = new XMLHttpRequest();
xhr.open('POST', 'url', true);
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
xhr.setRequestHeader('Authorization', 'Basic ' + 'auth');
var data = 'To=whatsapp:number&From=whatsapp:14155238886&ContentSid=sid&ContentVariables=%7B%221%22%3A%22409173%22%7D';
xhr.send(data);
xhr.onload = function () {
  if (xhr.status >= 200 && xhr.status < 300) {
    console.log('Success:', xhr.status, JSON.parse(xhr.responseText));
  } else {
    console.error('Request failed with status:', xhr.status, xhr.responseText);
  }
};
