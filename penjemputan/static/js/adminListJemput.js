$(document).ready(function(){
    $.get("/penjemputan/json/", function(data){
        let dataPenjemputanAdmin = '<div class="card-group">';
        dataPenjemputanAdmin += '<div class="row row-cols-1 row-cols-md-3 g-4">';
        for (let i = 0; i < data.length; i++) {
            let message = data[i].fields.is_finished ? 'sudah diambil':'Belum diambil';
            let color = data[i].fields.is_finished ? 'blue':'red';
            let id = data[i].pk;
            dataPenjemputanAdmin += '<div class="card border-info mb-5" style="width: 18rem;">'
            dataPenjemputanAdmin += '<div class="card-body">'
            dataPenjemputanAdmin += '<h5 class="card-title">' + data[i].fields.tanggal_jemput + '</h5>';
            dataPenjemputanAdmin += '<p class="card-text">' + data[i].fields.waktu_jemput + '</p>';
            dataPenjemputanAdmin += '<p class="card-text">' + data[i].fields.jenis_sampah + '</p>';
            dataPenjemputanAdmin += '<p class="card-text">' + data[i].fields.berat_sampah + '</p>';
            dataPenjemputanAdmin += '<p class="card-text"> ditambahkan pada ' + data[i].fields.waktu_sekarang + '</p>';
            dataPenjemputanAdmin += '<p class="card-text">' + data[i].fields.alamat + '</p>';
            dataPenjemputanAdmin += '<p class="card-text">Status: <span style="color:'+color+'">'+message+'</span></p>';
            dataPenjemputanAdmin += '<a href="update/'+id+'"><button class="updateBTN">Update</button></a>';
            dataPenjemputanAdmin += '<a href="delete/'+id+'"><button class="deleteBTN">Delete</button></a>';
            dataPenjemputanAdmin += '</div>';
            dataPenjemputanAdmin += '</div>';
        }
        dataPenjemputanAdmin += '</div>';
        dataPenjemputanAdmin += '</div>';
        document.getElementsByClassName("adminCardPenjemputan")[0].innerHTML = dataPenjemputanAdmin;
    });
});