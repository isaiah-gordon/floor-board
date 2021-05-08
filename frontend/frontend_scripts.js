var cc = document.getElementById('iframe').contentWindow;

function play_audio(){
    setInterval(function(){
        var audio = document.getElementById("audio");
        audio.play();
    }, 1800000);
}

function toggle_debugger(){
  var x = document.getElementById("debug_buttons");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

eel.expose(startProgress)
function startProgress(id, duration) {
    document.getElementById(id).style.animation="progress-animation "+duration+"s linear forwards";
}

eel.expose(resetProgress)
function resetProgress(id) {
    document.getElementById(id).style.animation="reset-animation 1s linear";
}

eel.expose(processProgress)
function processProgress(id) {
    document.getElementById(id).style.animation="process-animation 1s infinite";
}

eel.expose(updateHeader)
function updateHeader(id, text){
  var subtitle = document.getElementById(id);
  subtitle.innerHTML = text;
}

eel.expose(get_header)
function get_header(id){
  var subtitle = document.getElementById(id);
  return subtitle.textContent;
}

eel.expose(update_banner)
function update_banner(source){
  var banner = document.getElementById('banner');
  banner.src = source;
}

eel.expose(load)
function load(html_file){
  document.getElementById('iframe').src=html_file;
}

eel.expose(setCountdownImage)
function setCountdownImage(product){
    cc.setCountdownImage(product)
}

eel.expose(countdown)
function countdown(minute_to_the_hour) {
  cc.currentTime(minute_to_the_hour)
}

eel.expose(addNames)
function addNames(name0, name1, name2) {
  cc.addNames(name0, name1, name2)
}

eel.expose(product_add)
function product_add(product, a1, a2) {
  cc.smartAdd(product, a1, a2)
}

eel.expose(update_transactions)
function update_transactions(section, transactions){
  cc.updateTransactions(section, transactions)
}

eel.expose(subtract_product)
function subtract_product(product, a1, a2) {
  cc.subtractDonut(product, a1, a2)
}

eel.expose(get_results)
function get_results(){
    return cc.get_results();
}

eel.expose(display_results)
function display_results(container_specs) {
  cc.display_results(container_specs)
}
