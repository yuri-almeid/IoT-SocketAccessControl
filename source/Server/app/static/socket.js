function clearContents(element) {
    element.value = '';
}

function update_table(data) {
            
    var table = document.getElementById('tableinput');

    table.innerHTML = ''; 

    var total = data.length;

    var rpion = 0;

    for (var i = 0; i < total; i++) {
        var tr = document.createElement('tr');
        var td1 = document.createElement('td');
        var td2 = document.createElement('td');
        var td3 = document.createElement('td');
        var td4 = document.createElement('td');
        var td5 = document.createElement('td');
        var sp = document.createElement('span');
        var si = document.createElement('i');
        var td6 = document.createElement('td');

        // #
        td1.textContent = i + 1;
        // status
        sp.setAttribute('class', 'dot');
        
        if (data[i][0] == 'Online'){
            si.setAttribute('class', 'bg-success');
            rpion = rpion + 1;
        } else {
            si.setAttribute('class', 'bg-danger');
        }
        sp.textContent = data[i][0];
        // code
        td3.textContent = data[i][1];
        // store
        td4.textContent = data[i][2];        
        // ping
        td5.textContent = data[i][3];
        // Access
        td6.textContent = data[i][4];
        

        td2.appendChild(sp)
        sp.prepend(si)
        
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);
        tr.appendChild(td6);

        table.appendChild(tr);

     }


     var cardrpion = document.getElementById('raspon');
     var cardrpioff = document.getElementById('raspoff');

     cardrpion.textContent = rpion;
     cardrpioff.textContent = total - rpion;
     
     var percent_stat = document.getElementById('percent-online');

     percent_stat.innerHTML = ''; 

     var p_ = document.createElement('p');
     var sp_fr = document.createElement('span');
     var dv_progress = document.createElement('div');
     var dv_bg = document.createElement('div');

     var percent = (rpion/total)*100

     percent = percent.toFixed(1);

     var str_percent = percent + '%';
     p_.textContent = 'Sistemas Online';
     sp_fr.setAttribute('class', 'float-right');
     sp_fr.textContent = str_percent;


     dv_progress.setAttribute('class', 'progress');
     if (percent <= 25){
        dv_bg.setAttribute('class', 'bg-danger');
     } else if (percent > 25 && percent <= 85) {
        dv_bg.setAttribute('class', 'bg-warning');
     } else {
        dv_bg.setAttribute('class', 'bg-success');
     }
     dv_bg.setAttribute('style', 'width: ' + str_percent);

     p_.appendChild(sp_fr);
     percent_stat.appendChild(p_);

     dv_progress.appendChild(dv_bg);
     percent_stat.appendChild(dv_progress);


    return
}


$(document).ready(function() {
    var socket = io();
    var outtext = document.getElementById('commandOUT');

    var list_table = []
    socket.on('connect', function() {
        socket.emit('my_event', {data: 'Status Conectado'});
        outtext.value = 'client@user:~$ \n'; 
    });

    socket.on('my_response', function(msg, cb) {
        $('#log').append('<br>' + $('<div/>').text('Recebido #' + msg.count + ': ' + msg.data).html());
        if (cb)
            cb();        
    });

    socket.on('get_output', function(msg, cb) {
        document.getElementById("commandOUT").value += msg.out + ' \n';
        if (cb)
            cb();
    });

    socket.on('update_dashboard', function(msg, cb) {
        list_table = msg.data;
        update_table(list_table)
    });

    socket.emit('update', {data: $('go').val()});

    $('form#clean_this').submit(function(event) {
        var outtext = document.getElementById('commandOUT');
        outtext.value = 'client@user:~$ \n'; 
        return false;
    });

    $('form#get_room').submit(function(event) {
        currentCod = $('#codmm_room').val();
        socket.emit('join', {room: $('#codmm_room').val()});
        outtext.value = 'client@user:~$ Connected to ' + $('#codmm_room').val() + '\n'; 

        return false;
    });

    $('form#send_cmd').submit(function(event) {
        var input = $('#cmd_text').val();
        document.getElementById("commandOUT").value += 'client@user:~$ ' + input + ' \n';
        socket.emit('send_cmd', {room: currentCod, data: $('#cmd_text').val()});
        return false;
    });

    $('form#reboot_this').submit(function(event) {
        document.getElementById("3_toogle").click();
        socket.emit('send_cmd', {room: currentCod, data: 'sudo reboot'});
        return false;
    });

    $('form#open_this').submit(function(event) {
        socket.emit('send_cmd', {room: currentCod, data: 'curl http://127.0.0.1:5003/abrir'});
        document.getElementById("commandOUT").value += 'client@user:~$ curl http://127.0.0.1:5003/abrir \n';
        return false;
    });


    $("#inputcond").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#tableinput tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });

    $("#online_button").on("click", function() {
        var value = "online";
        $("#tableinput tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });

    $("#offline_button").on("click", function() {
        var value = "offline";
        $("#tableinput tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });

    var ping_pong_times = [];
    var start_time;
    window.setInterval(function() {
        start_time = (new Date).getTime();
        $('#transport').text(socket.io.engine.transport.name);
        socket.emit('my_ping');
    }, 1000);

    socket.on('my_pong', function() {
        var latency = (new Date).getTime() - start_time;
        ping_pong_times.push(latency);
        ping_pong_times = ping_pong_times.slice(-30); 
        var sum = 0;
        for (var i = 0; i < ping_pong_times.length; i++)
            sum += ping_pong_times[i];
        $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
    });


    $('form#emit').submit(function(event) {
        socket.emit('my_event', {data: $('#emit_data').val()});
        return false;
    });

    $('form#update').submit(function(event) {
        socket.emit('update', {data: $('go').val()});
        return false;
    });

    $('form#broadcast').submit(function(event) {
        socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
        return false;
    });
    $('form#join').submit(function(event) {
        socket.emit('join', {room: $('#join_room').val()});
        return false;
    });
    $('form#leave').submit(function(event) {
        socket.emit('leave', {room: $('#leave_room').val()});
        return false;
    });
    $('form#send_room').submit(function(event) {
        socket.emit('my_room_event', {room: $('#room_name').val(), data: $('#room_data').val()});
        return false;
    });

    $('form#send_cmd').submit(function(event) {
        console.log($('#room_data2').val());
        socket.emit('my_cmd_event', {room: $('#room_name2').val(), data: $('#room_data2').val()});
        return false;
    });

    $('form#close').submit(function(event) {
        socket.emit('close_room', {room: $('#close_room').val()});
        return false;
    });
    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect_request');
        return false;
    });
});
