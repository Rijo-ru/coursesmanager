document.addEventListener('DOMContentLoaded', () => {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
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
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});


$(window).on('load',function(){
    $('.modal').modal({backdrop: 'static', keyboard: false});
    $(document).ready(function() {
        $('#list select').select2({
            cacheDataSource: [],
            placeholder: 'Выберите свою фамилию из списка',
            allowClear: true,
            minimumInputLength: 3,
            language: {
                errorLoading: function () {
                    return 'Результат не может быть загружен.';
                },
                inputTooLong: function (args) {
                    var overChars = args.input.length - args.maximum;
                    var message = 'Пожалуйста, удалите ' + overChars + ' символ';
                    if (overChars >= 2 && overChars <= 4) {
                        message += 'а';
                    } else if (overChars >= 5) {
                        message += 'ов';
                    }
                    return message;
                },
                inputTooShort: function (args) {
                    var remainingChars = args.minimum - args.input.length;

                    var message = 'Пожалуйста, введите ' + remainingChars + ' или более символов';

                    return message;
                },
                loadingMore: function () {
                    return 'Загружаем ещё ресурсы…';
                },
                maximumSelected: function (args) {
                    var message = 'Вы можете выбрать ' + args.maximum + ' элемент';

                    if (args.maximum  >= 2 && args.maximum <= 4) {
                        message += 'а';
                    } else if (args.maximum >= 5) {
                        message += 'ов';
                    }

                    return message;
                },
                noResults: function () {
                  return 'Ничего не найдено';
                },
                searching: function () {
                  return 'Поиск…';
                }
            },
            ajax: {
                method: 'POST',
                url:'/api/lecture/' + link_token + '/students/',
                dataType: 'json',
                delay: 250,
                data: (params) => {
                    let query = {
                        search: params.term,
                        page: params.page || 1
                    };
                    console.log(query);
                    return query;
                },
                processResults: (data) => {
                    console.log(data);
                    return {results: data.items.map((elem) => {
                        let key = Object.keys(elem)[0];
                        return {id: key, text: elem[key]};
                    }), pagination: data.pagination};
                },
            }
        });
        $('#list select').on('select2:opening', () => {
            if($('select[name="username"]').hasClass('is-invalid') || $('#list .input-group').hasClass('has-error')){
                $($('#list select').data('select2').$element).removeClass('is-invalid');
                $($('#list select').data('select2').$container).removeClass('has-error');
            }
        });
    });
    $('#list').hide();
    let tabState = {
        phone: 'phone',
        list: 'list'
    }
    let currentTabState = tabState.phone;
    var options =  {
      onChange: function(cep){
        if($('input[name="phone_number"]').hasClass('is-invalid')){
            document.querySelector('input[name="phone_number"]').className = 'form-control';
        }
      },
    };
    $('input[name="phone_number"]').mask('(000) 000-00-00', options);
    $('#tab-phone').popover({
        trigger: 'hover',
        title:'Номер телефона',
        content:'Отметиться с помощью номера телефона.',
        placement:"top"
    });
    $('#tab-list').popover({
        trigger: 'hover',
        title:'Выбрать из списка',
        content:'Отметиться, выбрав свою фамилию из списка.',
        placement:"top"
    });
    $('#tab-phone').on('click', (e) => {
        $('#message').text('Введите ваш номер телефона:');
        $('#list').hide();
        $('#phone').show();
        currentTabState = tabState.phone;
    });
    $('#tab-list').on('click', (e) => {
        $('#message').text('Найдите и выберите себя из списка студентов:');
        $('#phone').hide();
        $('#list').show();
        $('.select2').css('width', '100%');
        currentTabState = tabState.list;
    });
    $('#submit').on('click', (e) => {
        if (currentTabState === tabState.phone) {
            if ($('input[name="phone_number"]').cleanVal().match(/^\d{10}$/) === null) {
                $('#phone .invalid-feedback').text('Номер телефона должен состоять из 10 цифр (без кода страны).');
                $('input[name="phone_number"]').addClass('form-control is-invalid');
            }
            else{
                data = {phone_number: $('input[name="phone_number"]').cleanVal()};
                $('#spinner').show();
                $('#phone').hide();
                $.ajax({
                    type: 'POST',
                    url: document.URL,
                    data: data,
                    success: (data) => {
                        console.log(data);
                        $('.modal').modal('hide');
                        $('#success-main').show();
                    },
                    error: (data) => {
                        payload = data.responseJSON;
                        $('#phone .invalid-feedback').text(payload.error);
                        $('input[name="phone_number"]').addClass('form-control is-invalid');
                        $('#phone').show();
                    },
                    complete: (data) => {
                        $('#spinner').attr('style','display:none!important');
                    },
                });
            }
        }
        else if (currentTabState === tabState.list) {
            if ($('#list select').val().match(/^\d{1,}$/) === null) {
                $('#list .invalid-feedback').text('Пожалуйста выберите свое имя из списка.');
                $($('#list select').data('select2').$element).addClass('is-invalid');
                $($('#list select').data('select2').$container).addClass('has-error');
            }
            else{
                data = {student_id: $('#list select').val()};
                $('#spinner').show();
                $('#list').hide();
                $.ajax({
                    type: 'POST',
                    url: document.URL,
                    data: data,
                    success: (data) => {
                        console.log(data);
                        $('.modal').modal('hide');
                        $('#success-main').show();
                    },
                    error: (data) => {
                        payload = data.responseJSON;
                        $('#list .invalid-feedback').text(payload.error);
                        $($('#list select').data('select2').$element).addClass('is-invalid');
                        $($('#list select').data('select2').$container).addClass('has-error');
                        $('#list').show();
                    },
                    complete: (data) => {
                        $('#spinner').attr('style','display:none!important');
                    },
                });
            }
        }
    });
});