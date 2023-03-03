const UserName = document.getElementById("input-user")
const password = document.getElementById("input-userP")
const login = document.getElementById("login")

let authInfo = {}

function Validate (){
    let status = true
    if(UserName.value == "" ){
        UserName.style.borderColor = "red"
        status = false
    }
    if(password.value == ""){
        password.style.borderColor = "red"
        status = false
    }

    return status
}

login.addEventListener("click", (event) => {
    if(Validate()){

        authInfo = {
            user : UserName.value,
            password : password.value
        }

        fetch('/login', {
            method: 'POST',
            body: JSON.stringify(authInfo),
            headers: {
              'Content-Type': 'application/json'
            }
          })
        .then((response) => {
            console.log(response)
        })
    }
})