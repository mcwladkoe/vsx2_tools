(function() {
    'use strict';

    var pageFormProcessor = function (form_el) {
        var self = this;
        self.form_el = form_el;
        if ($(self.form_el).data('type') === 'add-symbol') {
            console.log(1);
            $(self.form_el).find('.inputarea').on('keyup', function (ev) {
                console.log('1');
                var s = '', result = '';
                for (s of $(this).val()) {
                    result += s + '\u0336';
                }
                $(self.form_el).find('.outputarea').val(result);
            });
        } else {
            $(self.form_el).on('submit', function (ev) {
                self.processAndChange(ev);
            });
        };
        $(self.form_el).find('.copy').on('click', function (ev) {
            ev.preventDefault();
            var $copyField = $(self.form_el).find('.outputarea');
            $copyField.removeAttr('disabled');
            $copyField.select();
            document.execCommand("copy");
            $copyField.attr('disabled', 'disabled');
            $.notify({
                message: $(this).data('success'),
            }, {
                type: 'success'
            });
        });
        $(self.form_el).find('.share').on('click', function (ev) {
            ev.preventDefault();
            var formatted_params = $(self.form_el).serialize();
            const el = document.createElement('textarea');
            el.value = ($("form").attr("share-url") || '') + '?' + formatted_params;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
            $.notify({
                message: $(this).data('success'),
            }, {
                type: 'success'
            });
        });
    };

    pageFormProcessor.prototype.processAndChange = function (event) {
        event.preventDefault();
        var self = this;
        $.ajax({
            method: "POST",
            url: $(self.form_el).attr("action"),
            data: $(self.form_el).serialize(),
            dataType: "json"
        }).done(function (data) {
            if (data && data.result) {
                $(self.form_el).find('.outputarea').val(data.result);
                return;
            }
            $.notify({
                title: 'Что-то пошло не так:(',
                message: 'Чтобы связаться нажмите тут',
                url: 'mailto:mcwladkoe@outlook.com',
                targer: '_blank'
            }, {
                type: 'danger'
            });
        }).fail(function () {
            $.notify({
                title: 'Что-то пошло не так:(',
                message: 'Чтобы связаться нажмите тут',
                url: 'mailto:mcwladkoe@outlook.com',
                targer: '_blank'
            }, {
                type: 'danger'
            });
        });
    }

    $(document).ready(function(){
        $('form').each(function () {
            new pageFormProcessor(this);
        });
    });
})();
