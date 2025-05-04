fetch("http://127.0.0.1:5000/GetAllEmployees")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then((data) => {
    let table = document.getElementById("employees-table");
    let newrow = "";
    data.forEach((employee) => {
      newrow = `
    <tr>
    <td>${employee.id}</td>
    <td>${employee.FirstName}</td>
    <td>${employee.LastName}</td>
    <td>${employee.Email}</td>
    <td>${employee.Username}</td>
    <td>${employee.BirthDate}</td>
    <td>${employee.Departement}</td>  
    <td><button class="btn btn-primary"  ><a href="/EmployeeInfo/${employee.id}" style="text-decoration: none; color:white">Edit</a></button></td>
    </tr>
    `;
      table.innerHTML += newrow;
    });
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });
