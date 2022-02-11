$(document).ready(function(){

    $(document).on('input', '.kw', function(){
        var clients_table = $('.clients_table')
        clients_table.empty()
        $.ajax({
            type:'GET',
            url:'/search_client',
            data:{'kw':$('.kw').val()},
            dataType: "json",
            success:function(response){
                if (response){
                    parsed_data = JSON.parse(response)
                    parsed_data.map((client)=>{
                        clients_table.append(
                                `
                                <tr>
                                <td>${client.pk}</td>
                            <td class="text-uppercase">${client.fields.first_name} ${client.fields.last_name}</td>
                            <td>${client.fields.email}</td>
                            <td>${client.fields.phone}</td>
                            <td>
                                <form method="GET" action="/set_client">
                                    <input hidden name="id" value="${client.pk}"/>
                                    <button type="submit" class=" m-0 btn btn-outline-danger btn-sm">SET</button>
                                </form>
                            </td>
                          </tr>
                            `
                        )
                    })
                }
                else{
                    clients_table.append(
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


