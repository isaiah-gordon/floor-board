var counts = [0, 0, 0];
const donutArray = ['apple-fritter.png','boston-cream.png','maple-caramel.png','sprinkles.png','strawberry-jelly.png']
const muffinArray = ['banana.png', 'carrot.png', 'fruit.png']

product_specs = {
  'vanilla_cone': {'multi': false, 'back_stack': true, 'foreground': 18, 'background': 80},
  'spicy_chicken': {'multi': false, 'back_stack': true, 'foreground': 8, 'background': 32},
  'donut': {'multi': donutArray, 'back_stack': false, 'foreground': 10, 'background': 45},
  'fry': {'multi': false, 'back_stack': true, 'foreground': 14, 'background': 49},
  'rmhc_fry': {'multi': false, 'back_stack': true, 'foreground': 45, 'background': 195},
  'hashbrown': {'multi': false, 'back_stack': true, 'foreground': 12, 'background': 48},
  'muffin': {'multi': muffinArray, 'back_stack': true, 'foreground': 10, 'background': 35},
  'pie': {'multi': false, 'back_stack': true, 'foreground': 6, 'background': 30},
  'cookie': {'multi': false, 'back_stack': true, 'foreground': 10, 'background': 45},
  'hot_drink': {'multi': false, 'back_stack': true, 'foreground': 7, 'background': 35}
}

function add_product(product, section, layer){
  counts[section] = counts[section] + 1;
  document.getElementById(section+'count').innerHTML = counts[section];
  var img = document.createElement('img');
  img.setAttribute('id', section+'product'+(counts[section]))
  img.className = product;

  if (product_specs[product]['multi'] != false){
    const product_random = product_specs[product]['multi'][Math.floor(Math.random() * product_specs[product]['multi'].length)];
    img.src = 'product_images/'+product+'/'+product_random;
  }
  else{
    img.src = 'product_images/'+product+".png";
  }

  if (product_specs[product]['back_stack'] == true) {
    img.style = "z-index: -" + counts[section] + ";";
  }
  var src = document.getElementById(layer);
  src.appendChild(img);
}

eel.expose(subtract_product)
function subtract_product(product, section, amount){
  var subtracted = 0;
  while (subtracted < amount) {
    if (counts[section]<=product_specs[product]['background']) {
      var element = document.getElementById(section+'product'+(counts[section]));
      element.parentNode.removeChild(element);
      counts[section] = counts[section] - 1;
      document.getElementById(section+'count').innerHTML = counts[section];
    }
    else{
      counts[section] = counts[section] - 1;
      document.getElementById(section+'count').innerHTML = counts[section];
    }
    ++subtracted
  }

}

eel.expose(smartAdd)
function smartAdd(product, section, amount){
  var added = 0;
  while (added < amount) {
    if (counts[section]>=product_specs[product]['background']) {
      counts[section] = counts[section] + 1;
      document.getElementById(section+'count').innerHTML = counts[section];
    }
    else if (counts[section]<product_specs[product]['foreground']) {
      add_product(product, section, section+'foreground');
    }
    else if (counts[section]>=product_specs[product]['foreground']) {
      add_product(product, section, section+'background');
    }
    ++added
  }
}

function updateTransactions(section, transactions){
  document.getElementById(section+'transactions').innerHTML = transactions;
}

function addNames(name0, name1, name2){
  for (i = 0; i < 3; i++){
    document.getElementById(i + 'primary-label').innerHTML = arguments[i];
  }
}

function startProgress(id, duration) {
    document.getElementById(id).style.animation="progress-animation "+duration+"s linear forwards";
}

function resetProgress(id) {
    document.getElementById(id).style.animation="reset-animation 1s linear";
}

function get_results(){
    return counts;
}
