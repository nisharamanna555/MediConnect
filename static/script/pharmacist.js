var table = document.getElementById('resultTable');
var currentPage = page; // page where the current user is

$(document).ready(function(){
    load_data();
    function load_data(query)
    {
        $.ajax({
            url:'/searchResult',
            method:'POST',
            data:{query:query},
            success:function(data)
            {
                // pagination
                let numPerPage = 10;    // number of rows per page
                let maxPage = Math.ceil(Object.keys(data).length / numPerPage); // maximum number of page
                var pagination = document.getElementById("pageNum");
                pagination.innerHTML = "";
                if(currentPage < 6) {
                    let i = 1;
                    while(i <= maxPage && i <= 5) {
                        if(i === currentPage) { pagination.innerHTML += "<a class='pageNum' href='/pharmacy/page="+ i +"'><b>" + i + "</b> </a>"; }
                        else { pagination.innerHTML += "<a class='pageNum' href='/pharmacy/page="+ i +"'>" + i + " </a>"; }
                        i++;
                    }
                    if(maxPage > 5) {
                        pagination.innerHTML += "<a class='pageNum' href='/pharmacy/page=6'>></a>";
                    }
                } else {
                    pagination.innerHTML += "<a class='pageNum' href='/pharmacy/page="+ (currentPage-3) +"'>< </a>";
                    let i = currentPage - 2;
                    while(i <= maxPage && i <= currentPage+2) {
                        if(i === currentPage) { pagination.innerHTML += "<a class='pageNum' href='/pharmacy/page="+ i +"'><b>" + i + "</b> </a>"; }
                        else { pagination.innerHTML += "<a class='pageNum' href='/pharmacy/page="+ i +"'>" + i + " </a>"; }
                        i++;
                    }
                    if(maxPage > currentPage+2) {
                        pagination.innerHTML += "<a class='pageNum' href='/pharmacy/page="+ (currentPage+3) +"'>></a>";
                    }
                }
        
                // show data on table
                let i = 0;
                let rowNum = 1;
                table.innerHTML = "<tr><th>First Name</th><th>Last Name</th><th>Living City</th></tr>";
                for(let id in data) {
                    if(i < currentPage*numPerPage && i >= (currentPage-1)*numPerPage) {
                        let row = table.insertRow(rowNum);
                        row.style.cursor = "pointer";
                        row.addEventListener('click', function() {
                            window.location.href = '/pharmacyPatientDetails?patient_id='+id.toString();
                        });
                        let firstName = row.insertCell(0);
                        firstName.innerHTML = data[id].first_name;
                        let lastName = row.insertCell(1);
                        lastName.innerHTML = data[id].last_name;
                        let livingCity = row.insertCell(2);
                        livingCity.innerHTML = data[id].city;
                        rowNum++;
                    }
                    i++;
                }
            }
        });
    }
    $('#searchButton').click(function(event){
        event.preventDefault();
        var search = $('#searchText').val();
        currentPage = 1;
        if(search){
            load_data(search);
        } else {
            load_data();
        }
    });
});

console.log(page);