/**
 * Created by WillieTran on 7/29/14.
 */


$(document).ready(function() {

    function validateFirstPart() {
        if ($('#id_username').val().length < 0 && $('#id_name').val().length < 0) {
            alert("Username and name must be filled");
            return false;
        } else {
            return true;
        }
    }

    $(document).on('click', '#usernameNext', function() {
        if(validateFirstPart()) {
            $('.userName').hide();
            $('.emailPassword').fadeIn('slow')
        }
    });

    $(document).on('click', '.emailPasswordNext', function() {
        $('.emailPassword').hide();
        $('.aboutSection').fadeIn('slow')
    });

    $(document).on('click', '.aboutNext', function() {
        $('.aboutSection').hide();
        $('.imageSection').fadeIn('slow');
        $('.doneButton').show();
        $('.progressDone').show();
    });
});