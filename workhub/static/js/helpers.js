function clear_search_company_search_query(session_action, param) {
    var full_last_page = document.referrer;
    var last_page = full_last_page.split('/')
    if (last_page[last_page.length - 1] === 'statistics.php' ||
        last_page[last_page.length - 1] === 'search_company.php' ||
        last_page[last_page.length - 1] === 'enter.php') {
        $.ajax({
            url: "/company/action_region_filter",
            type: "GET",
            data: {
                session_action: session_action,
                region_to_session: param
            },
            cache: false,
            success: function (response) {}
        });
    }
}
