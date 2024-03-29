var ulTag = document.getElementById("myUL")
const totalDays = 50;
const totalAbsentDaysArray = []
let totalAbsentDays = null

document.getElementById("stats-button").style.display = "none"

let Students = []
let suggestion = []

fetch("/students.json")
    .then(response => response.json())
    .then(data => {
      Students = data
      console.log(Students)
      for(let i=0; i < Students.length; i++){
        suggestion.push(Students[i]['matricNum'])
    }
    
     let number_of_males = Students.filter(item => {
      return item.gender == "Male"
    })

    let number_of_females = Students.filter(item => {
      return item.gender == "Female"
    })

    console.log(suggestion)
    console.log(number_of_males.length)
    console.log(number_of_females.length)
    donut(number_of_males.length, number_of_females.length)
    })

function donut (present, absent) {
  bindto: "#donut"
  chart = c3.generate({
    data: {
        columns: [
            ['Male', present],
            ['Female', absent],
        ],
        type : 'donut',
    },
    donut: {
        title: "Attendance Rate"
    }
  });
 }


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
}

Students.forEach((item) => {
  totalAbsentDaysArray.push(item.absent)
})

totalAbsentDaysArray.forEach(item => {
    totalAbsentDays += item
})


let inputField = document.querySelector("#myInput")
let listBox = document.querySelector("#list")

function showData(list){
  let listData
    if(!list.length){
        listData = ""
    }else{
      listData = list.join(" ")
    }
    listBox.innerHTML = listData
}

inputField.onkeyup = (e) => {
  let search = e.target.value
  let valueR = []

  if(search){
    valueR = suggestion.filter( (data) => {
      return data.toLocaleLowerCase().startsWith(search.toLocaleLowerCase())
  })
    valueR = valueR.map((data) => {
      return data = "<li" + " " + "class=" + `"list-none w-[400px] border shadow rounded mx-auto my-2 text-xl text-green-color py-2 cursor-pointer"` + `id="clicked"` + ">" + data + "</li>"
    })
  }
  showData(valueR)
  let allList = document.querySelectorAll("li");
  for (let i = 0; i < allList.length; i++) {
    allList[i].setAttribute("onclick", "takeID(this)")
    
  }

}

function takeID(element){
    const theID = element.textContent
    const theStudent = Students.filter((studentID) => {
      return studentID.id == theID
    })

    let name = theStudent[0].first_name + " " + theStudent[0].last_name

    console.log(theStudent)
    document.querySelector("#absent--daysnum").innerHTML = theStudent[0].absent + theStudent[0].sick;
    document.querySelector("#absent--text").innerHTML = "Total Days " + name + " was absent";
       document.querySelector("#sick--text").innerHTML = "Days " + name + " was sick"
       document.querySelector("#sick--daysnum").innerHTML = theStudent[0].sick 
       document.querySelector("#present--text").innerHTML = "Total Days " + name + " was Present"
       document.querySelector("#present").innerHTML = totalDays - (theStudent[0].sick + theStudent[0].absent)
       pieChart(totalDays - theStudent[0].absent, theStudent[0].absent, theStudent[0].sick)
       document.querySelector("#rate").innerHTML = "Rate at which " + name + " Attend Class"

}

let downloadButton = document.querySelector("#download")

// var xhr = new XMLHttpRequest();
// xhr.open('GET', 'test.csv', true);
// xhr.onreadystatechange = function() {
//   if (xhr.readyState === 4 && xhr.status === 200) {
//     var csv = xhr.responseText;
//     // Convert the CSV to XLSX
//     var workbook = XLSX.utils.book_new();
//     var worksheet = XLSX.utils.csv_to_sheet(csv);
//     XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
//     XLSX.writeFile(workbook, 'output.xlsx');
//   }
// };
// xhr.send();


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


document.getElementById("myInput").onfocus = () =>{ 
 document.getElementById("myUL").style.display = "" 
  
 }

// document.getElementById("myInput").onblur = () => document.getElementById("myUL").style.display = "none"
document.getElementById("myInput").onkeyup = () => myFunction()


