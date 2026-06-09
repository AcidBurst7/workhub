/**
 * @package crm
 * @author  Andrew "Sossegado" Kliputa <andrew.amak@gmail.com>
 */
function get_regions_filter_list(text = "") {
    $.ajax({
        url: "/company/action_region_filter",
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: {
            q: text,
            region_name_sort: "",
            region_timezone_sort: ""
        },
        cache: false,
        success: function (response) {
            var data = JSON.parse(response).html
            $('#region-filtr').html('');
            if (data.length > 0) {
                $('#region-filtr').html(data);

                const regions = document.querySelectorAll("input[name='ch_regions[]']");
                for (const region of regions) {
                    region.addEventListener("click", function (e) {
                        $.ajax({
                            url: "/company/action_region_filter",
                            type: "POST",
                            headers: {'X-CSRFToken': csrftoken},
                            mode: 'same-origin',
                            data: {
                                session_action: e.srcElement.checked ? 'add' : 'delete',
                                region_to_session: e.srcElement.value
                            },
                            cache: false,
                            success: function (response) {}
                        });
                    });
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    var filter = document.querySelector('input#region_filter');
    filter.addEventListener('input', (evt) => {
        var text = evt.srcElement.value;

        //if (text.length > 0) {
            $('.region-timezone-sort-desc').css('display', 'none');
            $('.region-timezone-sort-asc').css('display', 'none');

            get_regions_filter_list(text);
        //}
    });

});

var region_sort_by_name = "region-name-asc";
$("#region-sort-by-name").click(function(e){
    e.preventDefault();

    if (e.target.ariaHidden == "region-name-desc") {
        e.target.ariaHidden = "region-name-asc";
        $('#region-sort-by-name-input').val("region-name-asc");

        $('.region-name-sort-desc').css('display', 'none');
        $('.region-name-sort-asc').css('display', 'inline');
    } else {
        e.target.ariaHidden = "region-name-desc";
        $('#region-sort-by-name-input').val("region-name-desc");

        $('.region-name-sort-desc').css('display', 'inline');
        $('.region-name-sort-asc').css('display', 'none');
    }

    region_sort_by_name = e.target.ariaHidden;

    $('.region-timezone-sort-desc').css('display', 'none');
    $('.region-timezone-sort-asc').css('display', 'none');

    $.ajax({
        url: "/company/action_region_filter",
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: {
            q: $('#region_filter').val(),
            region_name_sort: region_sort_by_name,
            region_timezone_sort: ""
        },
        cache: false,
        success: function (response) {
            var data = JSON.parse(response).html
            if (data) {
                $('#region-filtr').html('');
                $('#region-filtr').html(data);
            }
        }
    });
});


var region_sort_by_timezone = "region-timezone-asc";
$("#region-sort-by-timezone").click(function(e){
    e.preventDefault();

    if (e.target.ariaHidden == "region-timezone-desc") {
        e.target.ariaHidden = "region-timezone-asc";
        $('#region-sort-by-timezone-input').val("region-timezone-asc");

        $('.region-timezone-sort-desc').css('display', 'none');
        $('.region-timezone-sort-asc').css('display', 'inline');
    } else {
        e.target.ariaHidden = "region-timezone-desc";
        $('#region-sort-by-timezone-input').val("region-timezone-desc");

        $('.region-timezone-sort-desc').css('display', 'inline');
        $('.region-timezone-sort-asc').css('display', 'none');
    }

    region_sort_by_timezone = e.target.ariaHidden;

    $('.region-name-sort-desc').css('display', 'none');
    $('.region-name-sort-asc').css('display', 'none');

    $.ajax({
        url: "/company/action_region_filter",
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: {
            q: $('#region_filter').val(),
            region_name_sort: "",
            region_timezone_sort: region_sort_by_timezone
        },
        cache: false,
        success: function (response) {
            var data = JSON.parse(response).html
            if (data) {
                $('#region-filtr').html('');
                $('#region-filtr').html(data);
            }
        }
    });
});