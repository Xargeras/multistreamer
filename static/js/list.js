$(document).ready(function () {

    $("a.switcher").bind("click", function (e) {
        e.preventDefault();

        var theid = $(this).attr("id");
        var theproducts = $("ul#products");
        var classNames = $(this).attr('class').split(' ');

        if ($(this).hasClass("active")) {
            // if currently clicked button has the active class
            // then we do nothing!
            return false;
        } else {
            // otherwise we are clicking on the inactive button
            // and in the process of switching views!

            if (theid == "gridview") {
                $(this).addClass("active");
                $("#listview").removeClass("active");

                // remove the list class and change to grid
                theproducts.removeClass("list");
                theproducts.addClass("grid");
            } else if (theid == "listview") {
                $(this).addClass("active");
                $("#gridview").removeClass("active");

                // remove the grid view and change to list
                theproducts.removeClass("grid")
                theproducts.addClass("list");

            }
        }

    });
});
