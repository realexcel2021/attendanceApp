var ulTag = document.getElementById("myUL")
const totalDays = 50;
const totalAbsentDaysArray = []
let totalAbsentDays = null

document.getElementById("stats-button").style.display = "none"

let Students = []

fetch("/students.json")
    .then(response => response.json().then(response => {
      Students = response
      createElements(Students)
      document.querySelector("#absent--daysnum").innerHTML = Students.length
      document.querySelector("#attendance--daysnum").innerHTML = totalDays

      let maleList =  Students.filter(obj => obj.gender == "Male");
      let femaleList = Students.filter(obj => obj.gender == "Female");

      donut(maleList.length, femaleList.length)
    }))

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


function createElements(studentList) {
  studentList.forEach((item) => {
    let listItem = document.createElement("li");
    listItem.id = item.matricNum;
  
    let eachItem = document.createElement("a");
    eachItem.innerText = item.matricNum
    listItem.appendChild(eachItem)
    ulTag.appendChild(listItem)
    document.getElementById(listItem.id).onclick = () => {
      let studentID = listItem.id
          document.getElementById("myUL").style.display = "none" 
          document.getElementById("stats-button").style.display = ""
      console.log(studentID)
  
      if (studentID){
      let studentDetails = studentList.find((obj) => obj.id === studentID);
      const name = studentDetails.first_name + " " + studentDetails.last_name

       document.querySelector(".attendance").innerHTML = "Attendance Details for " + name;
       document.querySelector("#absent--daysnum").innerHTML = studentDetails.absent + studentDetails.sick;
       document.querySelector("#absent--text").innerHTML = "Days " + name + " was absent";
       document.querySelector("#sick--text").innerHTML = "Days " + name + " was sick"
       document.querySelector("#sick--daysnum").innerHTML = studentDetails.sick
       document.querySelector(".rate").innerHTML = "Rate at which " + name + " Attend Class"
       let totalAbsent = studentDetails.absent + studentDetails.sick
       pieChart(totalDays - totalAbsent, studentDetails.absent, studentDetails.sick)
  
    }
    }
  })
  
}

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


