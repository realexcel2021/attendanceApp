const theForm = document.getElementById("form")
var fname = document.getElementById("input-text")
var lName = document.getElementById("input-text-1")
var matricNum = document.getElementById("input-text-2")

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
   if (validate()){
        window.location.href = "success.html"
   }
})

