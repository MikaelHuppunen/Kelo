
function createTextElement(type, text) {
  let elem = document.createElement(type);
  elem.textContent = text;
  return elem;
}

function hide_Textbox(){
  let textBox = document.getElementById('container');
  textBox.style.display = 'none';
}

function get_wins(games, player){
  let wins = 0;
  for(let i = 0; i < games.length; i++){
    if((games[i][0] == player && games[i][2] == 1) || (games[i][1] == player && games[i][2] == -1)){
      wins++;
    }
  }
  return wins;
}

function get_draws(games, player){
  let draws = 0;
  for(let i = 0; i < games.length; i++){
    if((games[i][0] == player || games[i][1] == player) && games[i][2] == 0){
      draws++;
    }
  }
  return draws;
}

function get_losses(games, player){
  let losses = 0;
  for(let i = 0; i < games.length; i++){
    if((games[i][0] == player && games[i][2] == -1) || (games[i][1] == player && games[i][2] == 1)){
      losses++;
    }
  }
  return losses;
}

function get_results(games, player, played){
  return [get_wins(games,player), get_draws(games,player), get_losses(games,player)];
}

function print_stats(games, player, played){
  let [wins, draws, losses] = get_results(games, player, played);
  let black_text = document.getElementById('blackText');
  let green_text = document.getElementById('greenText');
  let gray_text = document.getElementById('grayText');
  let red_text = document.getElementById('redText');
  black_text.textContent = "Games " + played + ": ";
  green_text.textContent = " " + wins + " ";
  gray_text.textContent = " " + draws + " ";
  red_text.textContent = " " + losses + " ";
}

hide_Textbox();

function populateEloTable(data, games) {
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
        print_stats(games, name, played)
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

// Fetch the first file
fetch('kelo.txt')
  .then(response1 => response1.json())
  .then(data1 => {
    // Fetch the second file
    return fetch('games.txt')
      .then(response2 => response2.json())
      .then(data2 => populateEloTable(data1, data2));
  })


document.getElementById('filter-input').addEventListener('input', function(e) {
  filterEloTable(e.target.value);
});
