const theForm = document.getElementById("form")
var fname = document.getElementById("input-text")
var lName = document.getElementById("input-text-1")
var matricNum = document.getElementById("input-text-2")
var gender = document.getElementById("gender")
let arrivalState =  document.getElementById("absent")
const checkOut = document.getElementById("checkout")
const submitButton = document.getElementById("submitAttendance")
const Sick = document.getElementById("sick")

document.getElementById("adminLogin").addEventListener("click", () => {
    window.location.href = "/login"
})

checkOut.style.display = "none"

let studentData = null;

function validate() {
    let status = true
    if(fname.value == ''){
        fname.style.borderColor = 'red'
        status = false
    }
    if( lName.value == ''){
        lName.style.borderColor = 'red'
        status = false
    }
    if(matricNum.value == ''){
        matricNum.style.borderColor = 'red'
        status = false
    }
    
    return status
 }

 function validateAbsent(status){
    let valStatus = null
    if(status){
        valStatus = 1
    }else{
        valStatus = 0
    }
    return valStatus
 }

 function validatePresent(status1, status2){
    let valStatus = 0
    if(status1 == false || status2 == false){
        valStatus = 1
    }else{
        valStatus = 0
    }
    return valStatus
 }


theForm.addEventListener("click", (event) => {
    event.preventDefault();

   if (validate()){
        document.getElementById("names").innerText = fname.value + " " + lName.value;
        document.getElementById("matric").innerText = matricNum.value;
        document.getElementById("genderText").innerText = gender.value;
        checkOut.style.display = ""

        if(arrivalState.checked == true){
            document.getElementById("absentText").innerText =  " Marked Absent"
        }else{
            document.getElementById("absentText").innerText =  " Marked Present"
        }

        if(Sick.checked == true){
            document.getElementById("sickText").innerText =  " Student Reported sick"
            arrivalState.checked = false
        }else{
            document.getElementById("sickText").innerText =  " Student not Reported Sick"
        }

        let firstName = fname.value;
        let lastName = lName.value
        let capitalizedfName = firstName[0].toUpperCase() + firstName.slice(1);
        let capitalizedlName = lastName[0].toUpperCase() + lastName.slice(1);

        let studentDataObj = {
            id : matricNum.value.toUpperCase(),
            name : capitalizedfName + " " + capitalizedlName,
            matricNum : matricNum.value.toUpperCase(),
            gender : gender.value,
            absent : validateAbsent(arrivalState.checked),
            sick : validateAbsent(Sick.checked),
            gender : gender.value,
            present : validatePresent(arrivalState.checked, Sick.checked)
        }

       studentData = studentDataObj

        console.log(studentData)
   }


})

submitButton.addEventListener("click", () => {
    fetch('/people', {
        method: 'POST',
        body: JSON.stringify(studentData),
        headers: {
          'Content-Type': 'application/json'
        }
      })
    .then((response) => {
        console.log(response)
       
    })
    
})