document.addEventListener("DOMContentLoaded", function () {
  // Setting stop as grey to indicate the function is not running
  document.getElementById("stop-write").classList.add("bg-[#808080]");

  const startWriteBtn = document.getElementById("start-write");
  const stopWriteBtn = document.getElementById("stop-write");

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
});

// Function to send data for search and keystroke function
async function keystrokeData(counter) {
  if (counter == 1) {
    document.getElementById("start-write").classList.add("bg-[#808080]");
    document.getElementById("stop-write").classList.remove("bg-[#808080]");
  }
  if (counter == 0) {
    document.getElementById("start-write").classList.remove("bg-[#808080]");
    document.getElementById("stop-write").classList.add("bg-[#808080]");
  }

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