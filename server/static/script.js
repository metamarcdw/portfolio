
$(function() {
    $("#backlink").on("click", function() {
        window.history.back();
    });

    $("#delete-btn").on("click", function() {
        return window.confirm("Are you sure?");
    });
});
