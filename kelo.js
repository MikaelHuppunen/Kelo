
function createTextElement(type, text) {
  let elem = document.createElement(type);
  elem.textContent = text;
  return elem;
}

function hide_Textbox(){
  let textBox = document.getElementById('container');
  textBox.style.display = 'none';
}

hide_Textbox();

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
    let textElement = createTextElement('td', name);
    row.appendChild(textElement);

    let eloText = Math.round(elo*10)/10;
    if (played < 5) {
      eloText += '?';
    }

    row.appendChild(createTextElement('td', eloText));

    let textBox = document.getElementById('container');
    // Event listener for hover
    document.addEventListener('mousemove', function(e){
      let{left, top} = textElement.getBoundingClientRect();
      let computedStyle = getComputedStyle(textElement);
      // Get the width and height of the text
      let textWidth = textElement.offsetWidth;
      let textHeight = textElement.offsetHeight;

      if(e.clientX >= left && e.clientX <= left+textWidth && e.clientY >= top && e.clientY <= top + textHeight){
        textBox.style.display = 'initial';
        textBox.innerText = "Games: " + played;
      }
    });
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

document.addEventListener('mousemove', function(event){
  let textBox = document.getElementById('container');
  textBox.style.display = 'none';
  textBox.style.left = event.clientX + 'px';
  textBox.style.top = event.clientY + 'px';
});

fetch('kelo.txt')
  .then(response => response.json())
  .then(data => populateEloTable(data));


document.getElementById('filter-input').addEventListener('input', function(e) {
  filterEloTable(e.target.value);
});
