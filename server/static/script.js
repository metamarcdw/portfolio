'use strict';
(function() {

    var backlink = document.getElementById('backlink');
    if (backlink) {
        backlink.addEventListener('click', function() {
            window.location.href = document.referrer;
        });
    }

    var deleteButtons = document.getElementsByClassName('delete-btn');
    if (deleteButtons) {
        Array.prototype.forEach.call(deleteButtons, function(button) {
            button.addEventListener('click', function(e) {
                if (!window.confirm('Are you sure?'))
                    e.preventDefault();
            });
        });
    }

    var textArea = document.getElementsByClassName('simplemde')[0];
    if (textArea)
        var simplemde = new SimpleMDE({textArea});

    document.addEventListener('keypress', function(e) {
        if (e.ctrlKey && e.key === 'q') {
            var loginBtn = document.getElementById('btn-login');
            if (loginBtn) {
                if (loginBtn.classList.contains('hidden')) {
                    loginBtn.classList.remove('hidden');
                } else {
                    loginBtn.classList.add('hidden');
                }
            }
        }
    });

})();
