/**
 * Created by kevin on 8/14/2014.
 */

function getcalendar(user_id, selector){
    $.ajax({
        url: '/calendar/'+user_id,
        dataType: 'html',
        type: 'GET',
        success: function(response){
//            console.log(response);
            $(selector).html(response);
            $('#calendar').fadeIn('fast');
        }
    })
}


$(document).ready(function(){
    var id = $('#data').data('id');
    getcalendar(id, '#calendar_container');

    $(document).on('click', 'td', function(){
            var day = $(this).data('day');
            var hour = $(this).data('hour');
            var key = day+'-'+hour;
            if ($(this).hasClass('booked')){
                console.log('yeay');
                $(this).removeClass('booked');
                var i = schedule.indexOf(key);
                console.log(i);
                schedule.splice(i,1);
                console.log(schedule);
            }
            else {
                schedule.push(key);
                $(this).addClass("booked");
                console.log(schedule);
            }
        });

    $(document).on('click', '#submit_schedule', function(){
            console.log(schedule);
            var id = $(this).data('teacherid');
            var data = JSON.stringify(schedule);
            $.ajax({
                url:"/calendar/"+ id +"/",
                data:data,
                type:'POST',
                success: function(response){
                    $('#calendar_container').html(response);
                    console.log(response);
                    $('#calendar').fadeIn('fast');

                }
            })
        });
})