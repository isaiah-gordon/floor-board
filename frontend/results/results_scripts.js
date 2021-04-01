
function display_results(container_spec){

    var spec_number = 1;

    while (spec_number <= 3) {

      var container = document.getElementById('container' + spec_number)

      list = container_spec[spec_number]

      container.className = list[0];

      container.children[0].innerHTML = list[1];
      container.children[1].src = list[2];
      container.children[2].children[0].innerHTML = list[3];
      container.children[2].children[1].innerHTML = list[4];

      spec_number++

    }


}
