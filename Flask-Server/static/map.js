document.addEventListener("DOMContentLoaded", function () {
  // Function to fetch UID
  async function fetchUID() {
    try {
      const response = await fetch("http://127.0.0.1:5000/get_uid");
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
