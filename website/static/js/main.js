function searchCSSR() {
    var categ, input, filter, table, tr, td, i, txtValue;

    categ = document.getElementById("cssrCategory").value;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("tblResultCSSR");
    tr = table.getElementsByTagName("tr");

    for (i=0;i<tr.length;i++) {
        td = tr[i].getElementsByTagName("td")[categ];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}


function searchFunc() {
    var categ, input, filter, table, tr, td, i, txtValue;
        
    categ = document.getElementById("category").value;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("tblResult");
    tr = table.getElementsByTagName("tr");
    for (i=0;i<tr.length;i++) {
        td = tr[i].getElementsByTagName("td")[categ];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (categ == 1) {
                if (filter === '' || txtValue.toUpperCase() === filter) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            } else {
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            } 
        }
    }
}

