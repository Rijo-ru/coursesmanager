(function(SelectBox, SelectFilter) {
     window.addEventListener('load', function(e) {
        var SelectBoxMove = SelectBox.move;
        var SelectBoxMoveAll = SelectBox.move_all;
        SelectBox.move = (from, to) => {
            if ((from === 'id_students_from' && to === 'id_students_to')
                || (to === 'id_students_from' && from === 'id_students_to')
                || (from === 'id_register_students_from' && to === 'id_register_students_to')
                || (to === 'id_register_students_from' && from === 'id_register_students_to')){
                var is_append = to.endsWith('_to');
                var from_box = document.getElementById(from);
                var option;
                var boxOptions = from_box.options;
                var boxOptionsLength = boxOptions.length;
                for (var i = 0, j = boxOptionsLength; i < j; i++) {
                    option = boxOptions[i];
                    var option_value = option.value;
                    if (is_append){
                    if (option.selected
                        && SelectBox.cache_contains(from, option_value)
                        && !SelectBox.cache_contains('id_dropped_out_students_from', option_value)) {
                        SelectBox.add_to_cache('id_dropped_out_students_from', {value: option_value, text: option.text, displayed: 1});
                    }
                    }
                    else{
                    if (option.selected
                        && SelectBox.cache_contains(from, option_value)) {
                            if(SelectBox.cache_contains('id_dropped_out_students_from', option_value)){
                                SelectBox.delete_from_cache('id_dropped_out_students_from', option_value);
                            }
                            if(SelectBox.cache_contains('id_dropped_out_students_to', option_value)){
                                SelectBox.delete_from_cache('id_dropped_out_students_to', option_value);
                            }
                        }
                    }
                }
                if(!is_append){
                    SelectBox.redisplay('id_dropped_out_students_to');
                }
                SelectBox.redisplay('id_dropped_out_students_from');
                SelectFilter.refresh_icons('id_dropped_out_students');
            }
            SelectBoxMove(from, to);
        };
        SelectBox.move_all = (from, to) => {
            if ((from === 'id_students_from' && to === 'id_students_to')
                || (to === 'id_students_from' && from === 'id_students_to')
                || (from === 'id_register_students_from' && to === 'id_register_students_to')
                || (to === 'id_register_students_from' && from === 'id_register_students_to')){
                var is_append = to.endsWith('_to');
                var from_box = document.getElementById(from);
                var option;
                var boxOptions = from_box.options;
                var boxOptionsLength = boxOptions.length;
                for (var i = 0, j = boxOptionsLength; i < j; i++) {
                    option = boxOptions[i];
                    var option_value = option.value;
                    if (is_append){
                    if (SelectBox.cache_contains(from, option_value)
                        && !SelectBox.cache_contains('id_dropped_out_students_from', option_value)) {
                        SelectBox.add_to_cache('id_dropped_out_students_from', {value: option_value, text: option.text, displayed: 1});
                    }
                    }
                    else{
                    if (SelectBox.cache_contains(from, option_value)) {
                            if(SelectBox.cache_contains('id_dropped_out_students_from', option_value)){
                                SelectBox.delete_from_cache('id_dropped_out_students_from', option_value);
                            }
                            if(SelectBox.cache_contains('id_dropped_out_students_to', option_value)){
                                SelectBox.delete_from_cache('id_dropped_out_students_to', option_value);
                            }
                        }
                    }
                }
                if(!is_append){
                    SelectBox.redisplay('id_dropped_out_students_to');
                }
                SelectBox.redisplay('id_dropped_out_students_from');
                SelectFilter.refresh_icons('id_dropped_out_students');
            }
            SelectBoxMoveAll(from, to);
        };
     });
})(SelectBox, SelectFilter);