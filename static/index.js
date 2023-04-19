let Option, Validate, attendanceForm, submitButton, radioButton, matricNum, Notification

Validate = document.getElementById("validate")
attendanceForm = document.getElementById("attendanceForm")
Option = document.getElementById("selectedOpt")
submitButton = document.getElementById("submit")
radioButton = document.getElementsByName("attendance")
matricNum = document.getElementById("matric")
Notification = document.getElementById("notification");

function NotificationBar(form){
    if(Notification.style.opacity == '0'){
        Notification.style.opacity = '1'
    }

    if(form){
    Notification.style.display = 'block'
    Notification.style.backgroundColor = '#044801'
    document.getElementById("text").innerText = ' Attendance Marked Succesfully'

    }else{
        Notification.style.display = 'block'
        Notification.style.backgroundColor = 'red'
        document.getElementById("text").innerText = 'An error Occured'
    }

    setTimeout(() => {
        let Notification = document.getElementById("notification")
        Notification.style.opacity = "0"
       }, 2000);
}

attendanceForm.style.opacity = "0"

Validate.onclick = () => {

    if(matricNum.value == ""){
        NotificationBar(false)
    }else{
        let theVal = { matricNum : matricNum.value }
        console.log("The data to post")
        console.log(theVal)
        attendanceForm.style.opacity = "1"
        // fetch("/attendance", {
        //     method : "POST",
        //     body : JSON.stringify(theVal)
        // }).then((response) => {
        //     response.json()
        //     .then((data) => {
        //         Validate.disabled = true
        //         attendanceForm.style.opacity = "1"
        //         console.log(data)
        //     })
            
        // })
        // .catch(() => {
        //     NotificationBar(false)
        // })
    }
}

function validateForm () {
    let stat = false
    radioButton.forEach(element => {
        if(element.checked){
            stat = true
        }
    });
    return stat
}


submitButton.onclick = () => {
    console.log(validateForm())
    NotificationBar(validateForm())

    let submitObj = {}

    for(let i=0; i < radioButton.length; i++){
        if(radioButton[i].checked){
            submitObj = {
                ...submitObj,
                attendanceStatus : radioButton[i].value 
            }
        }
    }

    submitObj = {
        ...submitObj,
        [Option.value] : 1,
        id : matricNum.value
    }

    console.log(submitObj)

    fetch("/attendance", {
        method: "POST",
        headers : {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify(submitObj)
    })
    .then(response => {
        response.json()
        .then(data => console.log(data))
    })
    .catch(() => {
        NotificationBar(false)
    })

}
