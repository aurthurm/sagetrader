$(document).ready(function () {
  // statiticsStrategies
  $('select#statiticsStrategies').on('change', function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    var selected = $(this).val();
    var tableBody = $('#strategyStatsTable').find('tbody');
    $.ajax({
      method: "GET",
      url: "/trade/statistics/member",
      data: {
        'strategy': selected
      },
      success: function (res) {
        tableBody.html('');
        $('#dimpleChart').html('');
        console.log(res); // Table

        $.each(res, function (index, row) {
          tableBody.append(nano(template, row));
        }); // Dimple Js

        var bubblesvg = dimple.newSvg("#dimpleChart", 590, 400);
        var bubble = new dimple.chart(bubblesvg, res);
        bubble.setBounds(65, 30, 505, 330);
        bubble.addCategoryAxis("x", ["pair"]);
        bubble.addMeasureAxis("y", "rate");
        bubble.addMeasureAxis("z", "avg");
        bubble.addSeries("pair", dimple.plot.bubble);
        bubble.draw();
      } // End Success: ()

    });
  });
  var template = "<tr><td>{pair}</td><td>{trades}</td><td>{won}</td><td>{lost}</td><td>{pipsgained}</td><td>{pipslost}</td><td>{rate}</td></tr>";
}); // End of .ready()