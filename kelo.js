
function createTextElement(type, text) {
  let elem = document.createElement(type);
  elem.textContent = text;
  return elem;
}


function populateEloTable(data) {
  let table = document.getElementById('elo-table');
  let rank = 1;

  for (let i = 0; i < data.length; i++) {
    let [name, elo, played] = data[i];

    let row = table.insertRow(i);

    row['data-name'] = name;

    if(played >= 5){
      row.appendChild(createTextElement('td', rank + '.'));
      rank++;
    }else{
      row.appendChild(createTextElement('td'));
    }
    row.appendChild(createTextElement('td', name));

    let eloText = Math.round(elo*10)/10;
    if (played < 5) {
      eloText += '?';
    }

    row.appendChild(createTextElement('td', eloText));
  }
}

function filterEloTable(filter) {
  let table = document.getElementById('elo-table');

  for (let row of table.rows) {
    if (filter && !row['data-name'].toLowerCase().includes(filter.toLowerCase())) {
      row.hidden = true;
    } else {
      row.hidden = false;
    }
  }
}


fetch('kelo.txt')
  .then(response => response.json())
  .then(data => populateEloTable(data));


document.getElementById('filter-input').addEventListener('input', function(e) {
  filterEloTable(e.target.value);
});
