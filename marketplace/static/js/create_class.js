/**
 * Created by WillieTran on 7/29/14.
 */
$(document).ready(function() {

    $(function () {

    $(".basicInformation, .shortDescription, .longDescription, .imageSection").hide();

    $(".basicInformationLink, .shortDescriptionLink, .longDescriptionLink, .screenshotLink").bind("click", function () {

      $(".basicInformation, .shortDescription, .longDescription, .imageSection").hide();

      if ($(this).attr("class") == "basicInformationLink")
      {
        $(".basicInformation").show();
      }
      else if ($(this).attr("class") == "shortDescriptionLink")
      {
        $(".shortDescription").show();
      }
      else if ($(this).attr("class") == "longDescriptionLink")
      {
        $(".longDescription").show();
      }
      else
      {
        $('.imageSection').show();
      }
    });

});





});