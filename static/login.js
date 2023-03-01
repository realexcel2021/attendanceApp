const UserName = document.getElementById("input-user")
const password = document.getElementById("input-userP")
const login = document.getElementById("login")

let authInfo = {}

fetch('auth.json')
  .then(response => {
    // use the parsed data here
    
    console.log(response.headers)
  })
  .catch(error => console.error(error));

function Validate (){
    let status = true
    if(UserName.value == "" || UserName.value != authInfo.admin.username){
        UserName.style.borderColor = "red"
        status = false
    }
    if(password.value == "" || password.value != authInfo.admin.password){
        password.style.borderColor = "red"
        status = false
    }

    return status
}

login.addEventListener("click", (event) => {
    event.preventDefault()
    if (Validate()){
        window.location.href = "../templates/adminpage.html"
    }
})