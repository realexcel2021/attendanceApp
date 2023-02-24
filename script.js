  function myFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

document.getElementById("myUL").style.display = "none"


document.getElementById("myInput").onfocus = () =>{  document.getElementById("myUL").style.display = ""}
document.getElementById("myInput").onblur = () => document.getElementById("myUL").style.display = "none"
document.getElementById("myInput").onkeyup = () => myFunction()


$(document).ready(function() {
        
  columnColors = ['#9a4d6f', '#c76c47', '#f85115', '#d9b099', '#d4ba2f'];

  function setColumnBarColors(colors, chartContainer) {

    $('#' + chartContainer + ' .c3-chart-bars .c3-shape').each(function(index) {
      this.style.cssText += 'fill: ' + colors[index] + ' !important; stroke: ' + colors[index] + '; !important';
    });

    $('#' + chartContainer + ' .c3-chart-texts .c3-text').each(function(index) {
      this.style.cssText += 'fill: ' + colors[index] + ' !important;';
    });
  }

  var chart = c3.generate({
    bindto: '#designerChart',
    data: {
      columns: [
        ['attendance', 6, 8, 6, 5, 4]
      ],
      type: 'bar'
    },
    axis: {
      x: {
        label: {
          text: 'Famales',
          position: 'outer-center',
        },
        type: 'category',
        categories: ['Day_1', 'Day_2', 'Day_3', 'Day_4', 'Day_5'],
        tick: {
          centered: true
        }
      },
      y: {
        label: {
          text: 'Attendance (Days)',
          position: 'outer-middle'
        },
        max: 10,
        min: 0,
        padding: {
          top: 0,
          bottom: 0
        }
      }
    },
    legend: {
      show: false
    }
  });

  setColumnBarColors(columnColors, 'designerChart');

  // Color turns to original when window is resized
  // To handle that
  $(window).resize(function() {
    setColumnBarColors(columnColors, 'designerChart');
  });
});

function pieChart(d1, d2, d3){
  bindto: "#chart"
  var chart = c3.generate({
    data: {
        // iris data from R
        columns: [
            ['present', d1],
            ['absent', d2],
            ['sick', d3]
        ],
        type : 'pie',
        
    }
});


setTimeout(function () {
  chart.unload({
      ids: 'data1'
  });
  chart.unload({
      ids: 'data2'
  });
}, 2500);

}

function lineChart(){
  var chart = c3.generate({
    bindto: '#chart1',
    data: {
      columns: [
        ['data1', 30, 200, 100, 400, 150, 250],
        ['data2', 50, 20, 10, 40, 15, 25]
      ]
    }
});


}

  pieChart(12, 3, 10)
  lineChart()