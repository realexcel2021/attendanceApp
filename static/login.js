const UserName = document.getElementById("input-user")
const password = document.getElementById("input-userP")
const login = document.getElementById("login")

let authInfo = {}

fetch('auth.json')
  .then(response => response.json())
  .then(data => {
    // use the parsed data here
    authInfo = data
    console.log(data)
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
        const data = {
            username: UserName.value,
            password: password.value
        }

        fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                // window.location.href = "templates/adminPage.html"
                console.log("Logged in")
            } else {
                alert("Invalid username or password.")
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while processing your request.")
        });
    }
})