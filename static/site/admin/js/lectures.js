function clearSelectBox(from) {
        var from_box = document.getElementById(from);
        var option;
        var boxOptions = from_box.options;
        var boxOptionsLength = boxOptions.length;
        for (var i = 0, j = boxOptionsLength; i < j; i++) {
            option = boxOptions[i];
            var option_value = option.value;
            if (SelectBox.cache_contains(from, option_value)) {
                SelectBox.delete_from_cache(from, option_value);
            }
        }
        SelectBox.redisplay(from);
    };



document.addEventListener('DOMContentLoaded', () => {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = django.jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    django.jQuery.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var initialValue = django.jQuery('#id_course').val();
    django.jQuery('#id_course').data('previousValue', initialValue);



    django.jQuery('#id_course').on("change", () => {
        let elem = django.jQuery('#id_course');
        if (elem.val() !== elem.data('previousValue')) {

            clearSelectBox('id_register_students_from');
            clearSelectBox('id_register_students_to');

            clearSelectBox('id_dropped_out_students_from');
            clearSelectBox('id_dropped_out_students_to');

            clearSelectBox('id_teachers_from');
            clearSelectBox('id_teachers_to');

            django.jQuery.ajax({
                type: 'POST',
                url: '/api/students/',
                data: {'course': elem.val()}
            }).done((data) => {
                data.map((elem) => {
                    SelectBox.add_to_cache('id_register_students_from', {value: String(elem.id), text: elem.name, displayed: 1});
                });
            SelectBox.redisplay('id_register_students_from');
            SelectFilter.refresh_icons('id_register_students');
            });

            django.jQuery.ajax({
                type: 'POST',
                url: '/api/teachers/',
                data: {'course': elem.val()}
            }).done((data) => {
                data.map((elem) => {
                    SelectBox.add_to_cache('id_teachers_from', {value: String(elem.id), text: elem.name, displayed: 1});
                });
            SelectBox.redisplay('id_teachers_from');
            SelectFilter.refresh_icons('id_teachers');
            });
            django.jQuery('#id_course').data('previousValue', elem.val());

        }
    });
});