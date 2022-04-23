
$(document).ready(function(){
    $("#customers").on("click", "tr button", function(){
        let customer_id = $(this).closest("tr").find("td:eq(0)").text();
        delete_customer(customer_id);
    });
    $("#btn1").on("click", function(){
        get_customers();
    });
})


const get_customers =()=>{
    const get_customers_url = 'http://127.0.0.1:5000/customers';
    fetch(get_customers_url, {
        method: 'GET',
    }).then(response =>response.json())
      .then(customers=>{
        $("#customers").empty();
        let $header = $("<tr><th>ID</th><th>Name</th><th>Address</th><th>DELETE</th>");
        $("#customers").append($header)
            $.each(customers, function(index, cust){
                $("#customers").append(
                    $(`<tr>
                    <td>${cust.cust_id}</td>
                    <td>${cust.name}</td>
                    <td>${cust.address}</td>
                    <td><button>Delete</button></td>
                    </tr>`)

                );

            });
        });
    }

const add_customer =()=>{
    const add_customers_url = 'http://127.0.0.1:5000/customers';
    data = {
        name :$("#txt_name").val(),
        address :$("#txt_address").val()
    };
    fetch(add_customers_url, {
        method: 'POST',
        body: JSON.stringify(data) ,
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
          }
    }).then(response =>get_customers());
}

const get_customer_by_id =()=>{
    let customer_id =$("#txt_id_u").val();
    const get_customer_url = `http://127.0.0.1:5000/customers/${customer_id}`;
    fetch(get_customer_url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
          }
    }).then(response =>response.json())
    .then(customer =>{
        $("#txt_name_u").val(customer.name);
        $("#txt_address_u").val(customer.address);
    });
}

const update_customer =()=>{
    let customer_id =$("#txt_id_u").val();
    const upd_customers_url =`http://127.0.0.1:5000/customers/${customer_id}`;
    data = {
        name :$("#txt_name_u").val(),
        address :$("#txt_address_u").val()
    };
    fetch(upd_customers_url, {
        method: 'PUT',
        body: JSON.stringify(data) ,
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
          }
    }).then(response =>get_customers());
}


const delete_customer =(customer_id)=>{
    const delete_customer_url = `http://127.0.0.1:5000/customers/${customer_id}`;
    fetch(delete_customer_url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
          }
    }).then(response =>get_customers());
}

