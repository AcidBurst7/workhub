/**
 * @package crm
 * @author  Andrew "Sossegado" Kliputa <andrew.amak@gmail.com>
 */
function get_regions_filter_list(text = "", region_name_sort = "", region_timezone_sort = "") {
    $.ajax({
        url: "/company/action_region_filter/",
        type: "GET",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: {
            q: text,
            region_name_sort: region_name_sort,
            region_timezone_sort: region_timezone_sort
        },
        cache: false,
        success: function (response) {
            let regions_list = response["regions_list"];
            let selected_regions = response["selected_regions"];

            drawRegionsFilter(regions_list, selected_regions);
            addRegionsFilterListeners();
        }
    });
}

function drawRegionsFilter(regions_list, selected_regions) {
    $('#region-filtr').html('');
    let regions_html = "";

    if (regions_list.length > 0) {
        let class_region_description =  '';
        let timezone = '';
        let checked_region_input = '';
        for (let i = 0; i < regions_list.length; i++) {
            class_region_description = regions_list[i]['is_moving_out'] ? 'fw-bold' : '';
            timezone = regions_list[i]['timezone'] > 0 ? `+${regions_list[i]['timezone']}` : regions_list[i]['timezone'];
            
            checked_region_input = '';
            if (selected_regions.length > 0) {
                for (let j = 0; j < selected_regions.length; j++) {
                    if (regions_list[i]['id_region'] === parseInt(selected_regions[j])) {
                        checked_region_input = "checked";
                    }
                }
            }

            regions_html += `<div class="region" data-region="${regions_list['name_region']}" bis_skin_checked="1">` + 
                        `<input id="region${regions_list[i]['id_region']}" type="checkbox" name="ch_regions[]" ` +
                        `value="${regions_list[i]['id_region']}" ${checked_region_input}>` +
                        `<label for="region${regions_list[i]['id_region']}" class="px-2 ${class_region_description}">` +
                        `${regions_list[i]["name_region"]} (${timezone}) (${regions_list[i]['result_region_numrows']})` +
                        `</label></div>`;
        }
        $('#region-filtr').html(regions_html);
    }
}

function addRegionsFilterListeners() {
    const regions = document.querySelectorAll("input[name='ch_regions[]']");
    for (const region of regions) {
        region.addEventListener("click", function (e) {
            $.ajax({
                url: "/company/action_region_filter/",
                type: "GET",
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

document.addEventListener('DOMContentLoaded', () => {
    let filter = document.querySelector('input#region_filter');
    filter.addEventListener('input', (evt) => {
        let text = evt.srcElement.value;

        //if (text.length > 0) {
            $('.region-timezone-sort-desc').css('display', 'none');
            $('.region-timezone-sort-asc').css('display', 'none');

            get_regions_filter_list(text);
        //}
    });

});

let region_sort_by_name = "region-name-asc";
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

    get_regions_filter_list($('#region_filter').val(), region_sort_by_name, "");
});


let region_sort_by_timezone = "region-timezone-asc";
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

    get_regions_filter_list($('#region_filter').val(), "", region_sort_by_timezone);
});