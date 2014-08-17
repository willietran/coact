/**
 * Created by WillieTran on 7/29/14.
 */


$(document).ready(function() {

      $('.next').on('click', function () {
    var current = $(this).data('currentBlock'),
      next = $(this).data('nextBlock');

    // only validate going forward. If current group is invalid, do not go further
    // .parsley().validate() returns validation result AND show errors
    if (next > current)
      if (false === $('#register-form').parsley().validate('block' + current))
        return;

    // validation was ok. We can go on next step.
    $('.block' + current)
      .removeClass('show')
      .addClass('hidden');

    $('.block' + next)
      .removeClass('hidden')
      .addClass('show');

    $(document).on('click', '#id_image', function() {
        $('.doneButton').show();
        $('.progressDone').show();
    });

  });
});