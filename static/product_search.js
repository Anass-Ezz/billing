$(document).ready(function(){

    $(document).on('input', '.kw', function(){
        console.log('yeah')
        var products_container = $('.products_container')
        products_container.empty()
        $.ajax({
            type:'GET',
            url:'/product_search',
            data:{'kw':$('.kw').val()},
            dataType: "json",
            success:function(response){
                parsed_data = JSON.parse(response)
                if (parsed_data.length > 0){
                    console.log(response)
                    console.log(parsed_data.length)
                    parsed_data.map((product)=>{
                        products_container.append(
                            `
                            <div class="card">
                                <img
                                src="http://127.0.0.1:8000/data/${product.fields.image}                                "
                                class="card-img-top"
                                alt="..."
                                />
                                <div class="card-body">
                                    <h5 class="card-title text-uppercase">${product.fields.name} <span class="bg-info text-light ml-4 px-2" style="font-size: 11px; border-radius: 6px;" >${product.fields.quantity} item</span></h5>
                                    <a href="{% url 'main:detail' product.id %}" class="btn btn-danger btn-block">ADD TO BILL</a>
                                </div>
                            </div>
                            `
                        )
                    })
                }
                else{
                    console.log('noo')
                    products_container.append(
                        `
                        <tr>
                            <td colspan="5" style="width:100%; text-align:center;"><h1>NO RESULTS</h1></td>
                        </tr>
                        `
                    )

                }
            }
        })
    })

    // $('.client_search').submit((e)=>{
    //     e.preventDefault()
    //     var clients_table = $('.clients_table')
    //     clients_table.empty()
    //     $.ajax({
    //         type:'GET',
    //         url:'/search_client',
    //         data:{'kw':$('.kw').val()},
    //         dataType: "json",
    //         success:function(response){
    //             if (response){
    //                 parsed_data = JSON.parse(response)
    //                 parsed_data.map((client)=>{
    //                     clients_table.append(
    //                             `
    //                             <tr>
    //                             <td>${client.pk}</td>
    //                         <td class="text-uppercase">${client.fields.first_name} ${client.fields.last_name}</td>
    //                         <td>${client.fields.email}</td>
    //                         <td>${client.fields.phone}</td>
    //                         <td>
    //                             <form method="GET" action="/set_client">
    //                                 <input hidden name="id" value="${client.pk}"/>
    //                                 <button type="submit" class=" m-0 btn btn-outline-danger btn-sm">SET</button>
    //                             </form>
    //                         </td>
    //                       </tr>
    //                         `
    //                     )
    //                 })
    //             }
    //             else{
    //                 clients_table.append(
    //                     `
    //                     <tr>
    //                         <td colspan="5" style="width:100%; text-align:center;"><h1>NO RESULTS</h1></td>
    //                     </tr>
    //                     `
    //                 )

    //             }
    //         }
    //     })
    // })
    

});


