document.addEventListener("DOMContentLoaded", function () {
  const startWriteBtn = document.getElementById("start-write");
  const stopWriteBtn = document.getElementById("stop-write");
  const crudButton = document.getElementById("crudBtn");

  startWriteBtn.addEventListener("click", function () {
    console.log("Write started");
    startWriteBtn.disabled = true;
    stopWriteBtn.disabled = false;
  });

  stopWriteBtn.addEventListener("click", function () {
    console.log("Write stopped");
    startWriteBtn.disabled = false;
    stopWriteBtn.disabled = true;
  });

  crudButton.addEventListener("click", function(){
    window.location.href = "http://localhost:5000/map"
  })

  const form = document.getElementById("data-form");
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(form);
    const uid = formData.get("uid");
    const data = formData.get("data");
    console.log(`UID: ${uid}, Data: ${data}`);
  });

  // Function to fetch UID
  async function fetchUID() {
    try {
      const response = await fetch("/get_uid");
      const result = await response.json();
      if (result.uid) {
        document.getElementById("getuid").value = result.uid;
      }
    } catch (error) {
      console.error("Error fetching UID:", error);
    }
  }

  setInterval(fetchUID, 500);
});

// Function to send the user typed rollno to the flask server
async function postData() {
  try {
    const id = document.getElementById("getuid").value;
    const roll = document.getElementById("getrollno").value;

    console.log(id, roll);

    const response = await fetch("http://127.0.0.1:5000/postdata", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ rollno: roll, uid: id }),
    });

    const jsonResponse = await response.json();
    console.log(JSON.stringify(jsonResponse));

    if (jsonResponse.status) {  
      if (jsonResponse.status == "success") {
        alert("RollNo has been added");
      } else {
        alert("RollNo already mapped");
      }
    }

    document.getElementById("getrollno").value = "";
  } catch (error) {
    console.error(error);
  }
}

// Update data function
async function updateData(change) {
  try {
    
  }
  
  catch(error) {
    console.log(error)
  }
}

// Function to send data for search and keystroke function
async function keystrokeData(counter) {
  try {
    const response = await fetch("http://127.0.0.1:5000/keystrokeData", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ctr: counter }),
    });

    const jsonResponse = await response.json();
    console.log(JSON.stringify(jsonResponse));

    if (jsonResponse.status) {
      if (jsonResponse.status == "success") {
        console.log("Keystroke entered");
      } else {
        console.log("Keystroke entry failed/User not found");
      }
    }
  } catch (error) {
    console.error(error);
  }
}
