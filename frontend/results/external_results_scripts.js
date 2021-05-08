function display_results(result_specs){

    var spec_count = 1;
    var spec_amount = Object.keys(result_specs).length

    if (spec_amount >= 3){
      var row3 = document.getElementsByClassName('row3')
      for (var i = 0; i < row3.length; i++) {
        row3[i].style.display = "block";
      }
    }

    while (spec_count <= spec_amount) {

      console.log(spec_count);

      var row = document.getElementsByClassName('row' + spec_count)

      console.log(row);

      var rank = document.getElementById(spec_count + '-rank')
      var store = document.getElementById(spec_count + '-store')
      var image = document.getElementById(spec_count + '-image')
      var transactions = document.getElementById(spec_count + '-transactions')
      var total = document.getElementById(spec_count + '-total')

      list = result_specs[spec_count]

      rank.innerHTML = list[0];
      store.innerHTML = list[1];
      image.src = list[2]
      transactions.innerHTML = list[3]
      total.innerHTML = list[4]

      if (list[5] == true){
        for (var i = 0; i < row.length; i++) {
          row[i].style.backgroundColor = "rgba(25, 25, 25, 0.78)";
        }
      }

      spec_count++

    }


}

/*
{
1: ['1st', 'HEMLOCK SQUARE', 'https://dotops.app/image.jpg', '68', '3.45%', True]
2: ['2nd', 'LOWER SACKVILLE', 'https://dotops.app/image.jpg', '62', '3.15%', False]
3: ['3rd', 'BEDFORD HIGHWAY', 'https://dotops.app/image.jpg', '51', '3.08%', False]
}
*/
