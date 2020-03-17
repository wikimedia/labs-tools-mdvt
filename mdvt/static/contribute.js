$.get({
    url: '../api/get-media'
}).done(function(response) {
    $('.contribute-card').removeClass('loading');
    $('#img-link').attr('href', response.media_page);
    $('.contribute-card .card-img-top').attr('src', 'https://commons.wikimedia.org/wiki/Special:FilePath/' + response.media_title + '?width=500');
    $('#statement').html('<a href="https://www.wikidata.org/wiki/' + response.depict_id + '" target="_blank">' + response.depict_label + '</a> can be seen in the above <a href="' + response.media_page + '" target="_blank">image</a>');
    $('#media-title').html(response.media_title);
});
