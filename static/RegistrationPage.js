let matricNum, fName, lName, submitButton
let radio_geds_420, radio_itgy_402, radio_geds_400, radio_itgy_408, radio_itgy_312, radio_itgy_406
let radio_cosc_430, radio_geds_002

fName = document.getElementById("input--fName")
lName = document.getElementById("input--lName")
matricNum = document.getElementById("input--matricNum")
submitButton = document.getElementById("submit")

radio_geds_420 = document.getElementsByName("yes-geds_420")
radio_itgy_402 = document.getElementsByName("yes-itgy_402")
radio_geds_400 = document.getElementsByName("yes-geds_400")
radio_itgy_408 = document.getElementsByName("yes-itgy_408")
radio_itgy_312 = document.getElementsByName("yes-itgy_312")
radio_itgy_406 = document.getElementsByName("yes-itgy_406")
radio_cosc_430 = document.getElementsByName("yes-cosc_430")
radio_geds_002 = document.getElementsByName("yes-geds_002")

function Reset(){
    fName.value = ""
    lName.value = ""
    matricNum.value = ""

    let arr = [radio_geds_420, radio_itgy_402, radio_geds_400, radio_itgy_408, radio_itgy_312, radio_itgy_406, radio_cosc_430, radio_geds_002]
    
    arr.forEach((eachInput) => {
        for(let i=0; i < eachInput.length; i++){
            eachInput[i].checked = false
        }
    })

}

function NotificationBar(){
    let Notification = document.getElementById("notification")
    Notification.style.display = 'block'

    if(Notification.style.opacity == '0'){
        Notification.style.opacity = '1'
    }

    setTimeout(() => {
        let Notification = document.getElementById("notification")
        Notification.style.opacity = "0"
       }, 3000);
}

submitButton.onclick = () => {

    let arr = [radio_geds_420, radio_itgy_402, radio_geds_400, radio_itgy_408, radio_itgy_312, radio_itgy_406, radio_cosc_430, radio_geds_002]
    let pushobj = {}

    const  validateForm = () => {
        let response = false

        if(fName.value == ""){
            fName.style.borderColor = "red"
            response = false
        }else{
            pushobj = {
                ...pushobj,
                fName : fName.value
            }
        } 
        if(lName.value==""){
            lName.style.borderColor = "red"  
            response = false
        }else{
            pushobj = {
                ...pushobj,
                lName : lName.value
            }
            
        }
        if(matricNum.value == ""){
            matricNum.style.borderColor = "red" 
            response = false 
        }else{
            pushobj = {
                ...pushobj,
                matricNum : matricNum.value
            }
            response = true
        }
        return response
    }

    validateForm()

    let validateCourses = (val) => {
        if(val == "Yes"){
            return true
        }else {
            return false
        }
    }

    arr.forEach((each) => {
        for(let i=0; i < each.length; i++){
            if(each[i].checked){
                let key = each[i].name
                let obj = each[i].value

                pushobj = {
                    ...pushobj,
                    [key] : validateCourses(obj)
                }
                
            }
        }
    })

    if(validateForm()){
        fetch("/register", {
            method : "POST",
            body : JSON.stringify(pushobj)
        }).then(response => {
            response.json
            NotificationBar()
            Reset()
        })
        .then(data => console.log(data))
        
    }

}

