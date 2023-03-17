
function readfile(filepath){
    var result = null;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", filepath, false);
    xmlhttp.send();
    if (xmlhttp.status==200) {
        result = xmlhttp.responseText;
    }
    return result;
}

function createTextElement(type, text) {
  let elem = document.createElement(type);
  elem.textContent = text;
  return elem;
}

let data = JSON.parse(readfile("kelo.txt"));


let table = document.getElementById('elo-table');

for (let i = 0; i < data.length; i++) {
  let [name, elo, played] = data[i];

  let row = document.createElement('tr');

  row.appendChild(createTextElement('td', i + 1 + '.'))
  row.appendChild(createTextElement('td', name));

  let eloText = Math.round(elo*10)/10;
  if (played < 5) {
    eloText += '?';
  }
  row.appendChild(createTextElement('td', eloText));

  table.appendChild(row);
}
