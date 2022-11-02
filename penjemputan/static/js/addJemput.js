$(document).ready(function(){
    $('#submitBtn').click(function(){    
        let waktu_jemput = $('#id_waktu_jemput').val();
        let tanggal_jemput = $('#id_tanggal_jemput').val();
        let jenis_sampah = $('#id_jenis_sampah').val();
        let berat_sampah = $('#id_berat_sampah').val();
        let alamat = $('#id_alamat').val();
        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        $('#exampleModal').modal('hide');
        $.post("/penjemputan/add/", {
            tanggal_jemput: tanggal_jemput,
            waktu_jemput: waktu_jemput,
            jenis_sampah: jenis_sampah,
            berat_sampah: berat_sampah,
            alamat: alamat,
            csrfmiddlewaretoken: csrf_token
        }, function(data){
            $('.cardPenjemputan').empty();
            $.get("/penjemputan/json/", function(data){
                let dataPenjemputan = '<div class="card-group">';
                dataPenjemputan += '<div class="row row-cols-1 row-cols-md-3 g-4">';
                for (let i = 0; i < data.length; i++) {
                    let message = data[i].fields.is_finished ? 'sudah diambil':'Belum diambil';
                    let color = data[i].fields.is_finished ? 'blue':'red';
                    dataPenjemputan += '<div class="card border-info mb-5" style="width: 18rem;">'
                    dataPenjemputan += '<div class="card-body">'
                    dataPenjemputan += '<h5 class="card-title">' + data[i].fields.tanggal_jemput + '</h5>';
                    dataPenjemputan += '<p class="card-text">' + data[i].fields.waktu_jemput + '</p>';
                    dataPenjemputan += '<p class="card-text">' + data[i].fields.jenis_sampah + '</p>';
                    dataPenjemputan += '<p class="card-text">' + data[i].fields.berat_sampah + ' kg</p>';
                    dataPenjemputan += '<p class="card-text"> ditambahkan pada ' + data[i].fields.waktu_sekarang + '</p>';
                    dataPenjemputan += '<p class="card-text">' + data[i].fields.alamat + '</p>';
                    dataPenjemputan += '<p class="card-text">Status: <span style="color:'+color+'">'+message+'</span></p>';
                    dataPenjemputan += '</div>';
                    dataPenjemputan += '</div>';
                }
                dataPenjemputan += '</div>';
                dataPenjemputan += '</div>';
                document.getElementsByClassName("cardPenjemputan")[0].innerHTML = dataPenjemputan;
            });
        });
    });
});