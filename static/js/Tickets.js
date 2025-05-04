fetch("http://127.0.0.1:5000/GetTicketsWithResponse")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then((data) => {
    const section = document.getElementById("tickets-section");
    console.log("data", data);
    data.forEach((ticket) => {
      let newdiv = `<div><h3>${ticket.title}</h3>
      <p><span>Description:</span>${ticket.description}</p>
      <p><span>Category:</span>${ticket.category}</p>
      <p><span>From Date:</span>${ticket.Date}</p>
      `;
      if (ticket.response) {
        newdiv += `<h3>The Ticket Response :</h3>
        <p><span>Maintenance:</span>${ticket.response.response}</p>
        <p><span>More details:</span>${ticket.response.moredetails}</p>
        <p><span>End Date:</span>${ticket.To_Date}</p>
        `;
      }
      newdiv += `</div>`;
      section.innerHTML += newdiv;
    });
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });
