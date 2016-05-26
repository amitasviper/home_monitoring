function get_data(){
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    console.log("Sample : " + 'http://' + document.domain + ':' + location.port);
    socket.emit('channel_client_to_server', 'Ready i am fine');

    socket.on('channel_server_to_client', function (data) {

      console.log('Got data from server : ' + data);

      data = JSON.parse(data);

      var table = document.getElementById("table_info");
      for (var i = 0; i <table.rows.length; i++)
      {
        var house_id = table.rows[i].cells[0].innerHTML;
        house_id = house_id.trim();
        if(house_id != "House-id")
        {
            console.log(house_id);
            if(data.house_id == house_id)
            {
              var breakin = false;
                if (data.sensor_1 == 1)
                {
                  table.rows[i].cells[1].innerHTML = "Break-in";
                  breakin = true;
                }
                else
                {
                  table.rows[i].cells[1].innerHTML = "Normal";
                }

                if (data.sensor_2 == 1)
                {
                  table.rows[i].cells[2].innerHTML = "Break-in";
                  breakin = true;
                }
                else
                {
                  table.rows[i].cells[2].innerHTML = "Normal";
                }

                if (data.active == 1)
                {
                  table.rows[i].cells[3].innerHTML = "Active";
                }
                else
                {
                  table.rows[i].cells[3].innerHTML = "DISABLED";
                  table.rows[i].cells[1].innerHTML = "NA";
                  table.rows[i].cells[2].innerHTML = "NA";
                  table.rows[i].cells[4].innerHTML = "DISABLED";
                }
                
                if (breakin && data.active == 1)
                {
                  table.rows[i].cells[4].innerHTML = "UNSECURE";
                  table.rows[i].style.backgroundColor = "red";
                }
                else
                {
                  table.rows[i].style.backgroundColor = "green";
                  table.rows[i].cells[4].innerHTML= "SECURE";
                }
                if (data.active == 0) 
                {
                  table.rows[i].style.backgroundColor = "white";
                  table.rows[i].cells[4].innerHTML= "NA";
                };
            }
        }
      }
    } );
}

function initialise(){
	get_data();
}

$(document).ready(initialise);
