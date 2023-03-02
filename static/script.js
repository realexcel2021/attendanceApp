var ulTag = document.getElementById("myUL")
const totalDays = 120;
let studentID = null
let studentDetails = null
const totalAbsentDaysArray = []
let totalAbsentDays = null

fetch("/student.json")
    .then(response => console.log(response))

function donut (present, absent) {
  bindto: "#donut"
  chart = c3.generate({
    data: {
        columns: [
            ['present', present],
            ['absent', absent],
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


const Students = [
  {
    id : "QWE123",
    name : "Gray",
    matricNum : "QWE123",
    absent : 12,
    calledInSick : 9,
    gender : "male"
},
{
  id : "QWE124",
  name : "Mark",
  matricNum : "QWE124",
  absent : 9,
  calledInSick : 4,
  gender : "male"
},
{
  id : "QWE125",
  name : "David John",
  matricNum : "QWE125",
  absent : 50,
  calledInSick : 8,
  gender : "male"
},
{
  id : "QWE126",
  name : "Sheri Davis",
  matricNum : "QWE126",
  absent : 4,
  calledInSick : 0,
  gender : "female"
},
{
  id : "QWE127",
  name : "Duke Mark",
  matricNum : "QWE127",
  absent : 120,
  calledInSick : 0,
  gender : "female"
}
]

Students.forEach((item) => {
  totalAbsentDaysArray.push(item.absent)
})

totalAbsentDaysArray.forEach(item => {
    totalAbsentDays += item
})

console.log(totalAbsentDays)

Students.forEach((item) => {
  let listItem = document.createElement("li");
  listItem.id = item.matricNum;

  let eachItem = document.createElement("a");
  eachItem.innerText = item.matricNum
  listItem.appendChild(eachItem)
  ulTag.appendChild(listItem)
  document.getElementById(listItem.id).onclick = () => {
    studentID = listItem.id
        document.getElementById("myUL").style.display = "none" 
    console.log(studentID)

    if (studentID){
     studentDetails = Students.find((obj) => obj.id === studentID);
     document.querySelector(".attendance").innerHTML = "Attendance Details for " + studentDetails.name;
     document.querySelector("#absent--daysnum").innerHTML = studentDetails.absent;
     document.querySelector("#absent--text").innerHTML = "Days " + studentDetails.name + " was absent";
     document.querySelector("#sick--text").innerHTML = "Days " + studentDetails.name + " was sick"
     document.querySelector("#sick--daysnum").innerHTML = studentDetails.calledInSick
     document.querySelector(".rate").innerHTML = "Rate at which " + studentDetails.name + " Attend Class"
     let totalAbsent = studentDetails.absent + studentDetails.calledInSick
     pieChart(totalDays - totalAbsent, studentDetails.absent, studentDetails.calledInSick)

  }
  }
})

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

donut(totalDays, totalAbsentDays)
