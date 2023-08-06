(function ($) {
    if (!$) {
        $ = django.jQuery;
    }

    $.fn.showhide = function() {
        var markdowntoggle = $(this);
        var markdownxEditor = $(this).closest('.markdowntogglediv').find('.markdownx-editor');
        var markdownxPreview = $(this).closest('.markdowntogglediv').find('.markdownx-preview');
        if (markdowntoggle.prop('checked')) {
            markdownxEditor.show();
            markdownxPreview.hide();
            markdownxEditor.innerHeight(markdownxEditor.prop('scrollHeight'));
            $('button').prop('disabled', false);
        } else {
            markdownxEditor.hide();
            markdownxPreview.show();
            $('button').prop('disabled', true);
        }
    }


    $.fn.change_on_toggle = function() {
        return this.each( function() {
            var markdowntoggle = $(this);
            markdowntoggle.on('change.markdowntoggle', markdowntoggle.showhide);
        });
    };

    $(function() {
        $('.markdowntoggle').change_on_toggle();
        $('.markdowntoggle').showhide();
    });
})(jQuery);
