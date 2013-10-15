
function upgrade_pagination() {
    // change django-endless-pagination to bootstrap pagination
    $('#digg_pagination').children().each(function() {
        if ($(this).is('a')) {
            var text = $(this).html();
            var href = $(this).attr('href');
            $('#bootstrap_pagination').append('<li><a href="' + href + '">' + text + '</li>');
        } else {
            if ($(this).hasClass('endless_page_current')) {
                var text = $(this).children(':first').html();
                $('#bootstrap_pagination').append('<li class="active"><a href="#">' + text + '</li>');
            } else if ($(this).hasClass('endless_separator')) {
                var text = $(this).html();
                $('#bootstrap_pagination').append('<li class="disabled"><a href="#">' + text + '</li>');
            }
        }
    });
}

$(document).ready(function() {
    $('tbody.rowlink').rowlink();
    // $('[rel="tooltip"]').tooltip();
    upgrade_pagination();
})
