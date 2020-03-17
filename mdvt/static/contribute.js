$.get({
    url: '../api/get-media'
}).done(function(response) {
    $('.contribute-card').removeClass('loading');
    $('#img-link').attr('href', response.media_url);
    $('.contribute-card .card-img-top').attr('src', 'https://commons.wikimedia.org/wiki/Special:FilePath/' + response.media_title + '?width=800');
    $('#statement').html(response.depict_label + ' can be seen in the above image');
    $('#media-title').html(response.media_title);
});
