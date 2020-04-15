var filter_type = getUrlParam('filter-type', 'recent');
var filter_value = '';
switch (filter_type) {
    case 'category':
        filter_value = getUrlParam('category');
        break;
    case 'tag':
        filter_value = getUrlParam('tag');
        break;
}

var current_claim;

$.get({
    url: '../api/get-media',
    data: {
        filter_type: filter_type,
        filter_value: filter_value
    }
}).done(function(response) {
    if (response.status != "success") {
        show_toast('warning', 'Failed to get media.');
    } else {
        response = response.data;
        $('.contribute-card').removeClass('loading');
        $('#img-link').attr('href', response.media_page);
        $('.contribute-card .card-img-top').attr('src', 'https://commons.wikimedia.org/wiki/Special:FilePath/' + response.media_title + '?width=500');
        $('#statement').html('<a href="https://www.wikidata.org/wiki/' + response.depict_id + '" target="_blank">' + response.depict_label + '</a> can be seen in the above <a href="' + response.media_page + '" target="_blank">image</a>');
        $('#media-title').html(response.media_title);
        current_claim = response.claim_id;
    }
});

function post_contribution(status) {
    $.post({
        url: '../api/contribute',
        data: JSON.stringify({
            claim_id: current_claim,
            status: status
        }),
        contentType : 'application/json'
    }).done(function(response) {
        console.log(response);
    });
}

function show_toast(status, message) {
    var newToast = $('.' + status + '-toast-template').clone().removeClass(status + '-toast-template');
    newToast.find('.toast-body').text(message);
    newToast.appendTo('#toast-container');
    newToast.toast('show');
}

$('#true-btn').click(function() {
    post_contribution(true);
});

$('#false-btn').click(function() {
    post_contribution(false);
});

$('#skip-btn').click(function() {
    show_toast('warning', 'This function is not ready yet.');
});
