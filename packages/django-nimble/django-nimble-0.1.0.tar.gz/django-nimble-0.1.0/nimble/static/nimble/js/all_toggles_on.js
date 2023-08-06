(function ($) {
    if (!$) {
        $ = django.jQuery;
    }

    $(function() {
        $('.markdowntoggle').bootstrapToggle('on')
    });
})(jQuery);
