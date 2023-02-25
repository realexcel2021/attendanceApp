const theForm = document.getElementById("form");
const fname = document.getElementById("input-text");
const lName = document.getElementById("input-text-1");
const matricNum = document.getElementById("input-text-2");
const gender = document.getElementById("gender");
const absent = document.querySelector(".absent").checked;

const data = {
  first_name: fname.value,
  last_name: lName.value,
  matric_num: matricNum.value,
  gender: gender.value,
  status: absent ? 1 : 0,
};

const jsonData = JSON.stringify(data);

function validate() {
  let status = true;
  if (fname.value == "") {
    fname.style.borderColor = "red";
    status = false;
  }
  if (lName.value == "") {
    lName.style.borderColor = "red";
    status = false;
  }
  if (matricNum.value == "") {
    matricNum.style.borderColor = "red";
    status = false;
  }
  console.log(absent);
  return status;
}

theForm.addEventListener("submit", (event) => {
  event.preventDefault();
  fetch("http://127.0.0.1:5000/people", {
    method: "POST",
    body: jsonData,
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (validate()) {
        document.getElementById("names").innerText = fname.value + " " + lName.value;
        document.getElementById("matric").innerText = matricNum.value;
        document.getElementById("genderText").innerText = gender.value;
        document.getElementById("absentText").innerText = absent ? "Student Absent" : "Student Present";
      }
    })
    .catch((error) => console.log(error));
});