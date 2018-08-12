
$(function() {
    $("#backlink").on("click", function() {
        window.history.go(-1);
    });

    $(".delete-btn").on("click", function() {
        return window.confirm("Are you sure?");
    });
});
