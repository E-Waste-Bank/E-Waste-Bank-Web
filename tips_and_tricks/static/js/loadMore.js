  // Load More
  $(document).ready(function() {
    $("#loadmoreBtn").on('click', function() {
        var _currentResult = $(".post-box").length;
        $.ajax({
            url: "/tips-and-tricks/load-more",
            type: 'GET',
            data: {
                'offset': _currentResult,
            },
            dataType: 'json',
            success: function(res) {
                var _html = '';
                var json_data = $.parseJSON(res.posts);
                $.each(json_data, function(index, data) {
                    _html += `<div class="card p-3 mt-4 post-box" id="article-list">
                                <div class="row">
                                    <div class="col-md-4">
                                        <div class="position-relative">
                                        <img
                                            class="rounded w-100"
                                            height="300"
                                            src= ${data.fields.image_url}
                                        >
                                        </div>
                                    </div>

                                    <div class="col-md-8">
                                        <div class="mt-2">
                                            <div class="d-flex justify-content-between align-items-center" id="title">
                                                <h3 class="mb-1"> ${data.fields.title}</h3>
                                            </div>

                                            <div class="d-flex justify-content-md-start justify-content-between views-content mt-2">
                                                <div class="d-flex flex-row align-items-center" id="calendar"> 
                                                    <i class="fa fa-calendar"></i>
                                                    <h5 class="ms-1 views"> ${data.fields.published_date}</h5>
                                                    <h4 class="ms-1 views">|</h4>
                                                </div>

                                                <div class="d-flex flex-row align-items-center ms-2" id="source"> 
                                                    <i class="fa fa-user"></i> 
                                                    <h5 class="ms-1 views"> ${data.fields.source}</h5> 
                                                </div>
                                            </div>

                                            <p class="text-dark mt-3"> ${data.fields.brief_description}</p>

                                            <a class="btn btn-warning btn-md"
                                                id="button-readmore"
                                                target="_blank"
                                                href="${data.fields.article_url}"
                                                class="align-self-end btn btn-sm btn-block btn-dark"
                                                >Read More
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>`;
                });
                $("#replaceable-content").append(_html);
                var _countTotal = $(".post-box").length;
                if (_countTotal == res.totalResult) {
                    $("#loadmoreBtn").hide();
                }
                $("#loadmoreBtn").removeClass('disabled').text('Load More');
            }
        });
    });
});