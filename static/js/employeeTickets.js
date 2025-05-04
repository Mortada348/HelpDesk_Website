fetch("http://127.0.0.1:5000/EmployeeTickets")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then((data) => {
    const section = document.getElementById("employee-tickets");
    var newdiv;
    section.innerHTML = "";
    data.forEach((ticket) => {
      newdiv = `<div class="employee-ticket">
          <div id="title">
          <div class="small_card">
            <i class="fa-solid fa-reply" onclick="openForm('myForm-${ticket.id}')"></i>
          </div>
          <h3>${ticket.title}</h3>
          </div>
          <p>
            <span>Description :</span> ${ticket.description}
          </p>
          <div>
            <p><span>Category :</span> ${ticket.category}</p>
            <div class="form-popup" id="myForm-${ticket.id}">
              <form action="/AddResponse" class="form-container" method="post">
                <h1>Maintenance:</h1>
                <input type="hidden" name="ticket_id" value="${ticket.id}">
                <label for="description-${ticket.id}">Maintenance description:</label>
                <textarea name="response" id="description-${ticket.id}" cols="50" rows="10"></textarea>
                <label for="steps-${ticket.id}">Fault Maintenance Steps:</label>
                <textarea name="moredetails" id="steps-${ticket.id}" cols="50" rows="5"></textarea>
                <button type="submit" class="btn">Submit</button>
                <div class="small_card">
                <i class="fa-solid fa-xmark" onclick="closeForm('myForm-${ticket.id}')"></i>
                </div>
              </form>
            </div>
          </div>
        </div>`;
      section.innerHTML += newdiv;
    });
  });
