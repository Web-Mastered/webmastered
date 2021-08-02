jQuery(function($) {
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
    $('.portal-nav-item a').each(function() {
        if (this.href === path.split('?')[0]) {
            $(this).addClass('active');
        }
    });
});

$(document).ready( function () {
    $('#BrowserRequest24hDataTable').DataTable({
        "language": {
            "emptyTable": "Couldn't retrieve country traffic data due to low/no traffic"
        }
    })
});

$(document).ready( function () {
    $('#HourlyRequestDataTable').DataTable({
        pageLength: 24,
        paging: false,
        searching: false,
    })
});

$(document).ready( function () {
    $('#BrowserMap24hDataTable').DataTable({
        "language": {
            "emptyTable": "Couldn't retrieve browser traffic data due to low/no traffic"
        }
    })
});

$(document).ready( function () {
    $('#FirewallEventsDataTable').DataTable({
        "language": {
            "emptyTable": "There were no threats detected by the firewall"
        }
    })
});

$(document).ready( function () {
    $('#DNSRecordRequestDataTable').DataTable({
        "language": {
            "emptyTable": "You have not submitted any DNS records"
        }
    })
});

$(document).ready( function () {
    $('#FeatureRequestDataTable').DataTable({
        "language": {
            "emptyTable": "You have not submitted any feature requests"
        }
    })
});

$(document).ready( function () {
    $('#PrioritySupportSubmissionsDataTable').DataTable({
        "language": {
            "emptyTable": "You have not submitted any priority support submissions"
        }
    })
});



function sidenav_control_show(){
    $(".sidenav").removeClass("d-none")
    $(".sidenav").addClass("d-flex")
    $(".sidenav").addClass("w-100")
    $(".sidenav").addClass("high-z-index")
};

function sidenav_control_collapse(){
    $(".sidenav").removeClass("d-flex")
    $(".sidenav").removeClass("w-100")
    $(".sidenav").removeClass("high-z-index")
    $(".sidenav").addClass("d-none")
};   