/**
 * Created by WillieTran on 7/29/14.
 */
$(document).ready(function() {

    $(function () {

    $(".shortDescription, .longDescription, .imageSection").hide();

    $(".basicInformationLink, .shortDescriptionLink, .longDescriptionLink, .screenshotLink").bind("click", function () {

      $(".basicInformation, .shortDescription, .longDescription, .imageSection").hide();
      $(".basicInformationLink, .shortDescriptionLink, .longDescriptionLink, .screenshotLink").removeClass('active');

      if ($(this).attr("class") == "basicInformationLink")
      {
        $(".basicInformation").show();
        $(".basicInformationLink").addClass('active');
      }
      else if ($(this).attr("class") == "shortDescriptionLink")
      {
        $(".shortDescription").show();
        $(".shortDescriptionLink").addClass('active');
      }
      else if ($(this).attr("class") == "longDescriptionLink")
      {
        $(".longDescription").show();
        $(".longDescriptionLink").addClass('active');
      }
      else
      {
        $('.imageSection').show();
        $('.screenshotLink').addClass('active');
      }
    });
    });


    $('#id_title').on('focus', function() {
        $('.title-tip').show();
    });

    $('#id_title').focusout(function() {
        $('.title-tip').hide();
    });

    $('#id_project').on('focus', function() {
        $('.project-tip').show();
    });

    $('#id_project').focusout(function() {
        $('.project-tip').hide();
    });

    $('#id_cost').on('focus', function() {
        $('.price-tip').show();
    });

    $('#id_cost').focusout(function() {
        $('.price-tip').hide();
    });

    $('#id_short_description').on('focus', function() {
        $('.s-description-tip').show();
    });

    $('#id_short_description').focusout(function() {
        $('.s-description-tip').hide();
    });

    $('#id_description').on('focus', function() {
        $('.description-tip').show();
    });

    $('#id_description').focusout(function() {
        $('.description-tip').hide();
    });

    enteredText = $('#id_description').val();
    numberOfLineBreaks = (enteredText.match(/\n/g)||[]).length;
    characterCount = enteredText.length + numberOfLineBreaks;


});