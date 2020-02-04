$(document).ready(function () {
 // alert('gggggggggggggggg');
      $('form.short_product').on('change select', function () {
            $(this).closest("form").submit();
        });
      $('#sel_page').on('change', function() {  
           location.href = $(this).val();     
                });
 });