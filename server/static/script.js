
$(function() {
    $("#backlink").on("click", function() {
        window.location.href = document.referrer;
    });

    $(".delete-btn").on("click", function() {
        return window.confirm("Are you sure?");
    });
});
