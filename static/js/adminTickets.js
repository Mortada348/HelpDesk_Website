document.addEventListener("DOMContentLoaded", function () {
  getAllEmployees();
});

const getAllEmployees = () => {
  fetch("http://127.0.0.1:5000/GetTickets")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      const section = document.getElementById("admin-tickets");
      var newdiv;
      section.innerHTML = "";
      data.forEach((ticket) => {
        newdiv = `<div id="${ticket.id}"><h3 name="title">${ticket.title}</h3>
      <p name="description"><span>Description:</span>${ticket.description}</p>
      <p name="category"><span>Category:</span>${ticket.category}</p>
      <Select  id="allEmployees-${ticket.id}">
      </Select>
      <button id="${ticket.id}">Submit</button>
      </div>`;
        section.innerHTML += newdiv;
      });
    })
    .then(() => {
      fetch("http://127.0.0.1:5000/GetAllEmployees")
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          var newoption = "";
          data.forEach((employee) => {
            var allEmployeesElements = document.querySelectorAll(
              '[id^="allEmployees"]'
            );
            newoption = `<option value=${employee.id}>${employee.Username}</option>`;
            // select.innerHTML += newoption;
            allEmployeesElements.forEach((select) => {
              select.innerHTML += newoption;
            });
          });
        });
    });
};

const section = document.getElementById("admin-tickets");
function updateTicket(ticketId, employeeId) {
  fetch("http://127.0.0.1:5000/updateTicket", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ ticketId: ticketId, employeeId: employeeId }),
  })
    .then((response) => {
      getAllEmployees();

      throw new Error("Network response was not ok.");
    })
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
section.addEventListener("click", (event) => {
  const button = event.target;
  if (button.tagName === "BUTTON" && button.textContent === "Submit") {
    const ticketId = button.id;
    const employeeSelect = button.previousElementSibling;
    const employeeId = employeeSelect.value;
    updateTicket(ticketId, employeeId);
  }
});
