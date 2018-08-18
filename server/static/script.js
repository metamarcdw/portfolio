
$(function() {
    $("#backlink").on("click", function() {
        window.location.href = document.referrer;
    });

    $(".delete-btn").on("click", function() {
        return window.confirm("Are you sure?");
    });

    var element = $(".simplemde")[0];
    if (element) {
        var simplemde = new SimpleMDE({element});
    }

    $(document).keypress("q", function(e) {
        if (e.ctrlKey) {
            $("#btn-login").fadeToggle("slow");
        }
    });

});
