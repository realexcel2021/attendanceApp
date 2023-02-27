const theForm = document.getElementById("form")
var fname = document.getElementById("input-text")
var lName = document.getElementById("input-text-1")
var matricNum = document.getElementById("input-text-2")
var gender = document.getElementById("gender")
let arrivalState =  document.getElementById("absent")

const studentData = [];

var data = {
    name : "John Doe",
    matric_num : "WWQQ123",
    sex : "male",
    absent : 1
}


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


theForm.addEventListener("click", (event) => {
    event.preventDefault();
    // fetch('students.json', {
    //     method: 'POST',
    //     body: jsonData,
    //     headers: {
    //       'Content-Type': 'application/json'
    //     }
    //   })
    // .then(() => console.log(jsonData))
    // .then(response => response.json())
   if (validate()){
        document.getElementById("names").innerText = fname.value + " " + lName.value;
        document.getElementById("matric").innerText = matricNum.value;
        document.getElementById("genderText").innerText = gender.value;
        if(arrivalState.checked == true){
            document.getElementById("absentText").innerText =  " Marked Absent"
        }else{
            document.getElementById("absentText").innerText =  " Marked Present"
        }

   }


})


// window.location.href = "success.html"
