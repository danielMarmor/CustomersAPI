function showCustomers(){
    let $tblCustomers = $('#tblCustomers');
    const customers_data_url = 'http://127.0.0.1:5000/customers_data';
    $.ajax({url: customers_data_url}).then(function(response){
                // HEADER
         let customers = JSON.parse(response);
         $tblCustomers.empty();
         let $headerTemplate = $('<tr><th>CustomerId</th><th>Name</th><th>Address</th></tr>');
         $tblCustomers.append($headerTemplate);
                // DATA
         $.each(customers, function(index, cust){
              let $rowTemplate = `<tr><td>${cust.cust_id}</td>
                                      <td>${cust.name}</td>
                                      <td>${cust.address}</td>
                                  </tr>`;
              $tblCustomers.append($rowTemplate)
          });
    });
}


