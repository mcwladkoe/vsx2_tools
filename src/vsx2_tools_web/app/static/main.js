(function() {
    'use strict';

    const pageFormProcessor = function (form_el) {
        const self = this;
        self.$form_el = $(form_el);
        const dataType = self.$form_el.data('type');
        if (dataType === 'add-symbol') {
            self.$form_el.find('.inputarea').on('keyup', function () {
                let result = '';
                for (const s of $(this).val()) {
                    result += s + '\u0336';
                }
                self.$form_el.find('.outputarea').val(result);
            });
         } else {
            self.$form_el.on('submit', function (ev) {
                self.processAndChange(ev);
            });
        }

        self.$form_el.find('.copy').on('click', function (ev) {
            ev.preventDefault();
            var $copyField = self.$form_el.find('.outputarea');
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
    };

    pageFormProcessor.prototype.processAndChange = function (event) {
        event.preventDefault();
        const self = this;
        $.ajax({
            method: "POST",
            url: self.$form_el.attr("action"),
            data: self.$form_el.serialize(),
            dataType: "json"
        }).done(function (data) {
            if (data && data.result) {
                self.$form_el.find('.outputarea').val(data.result);
                return;
            }
            $.notify({
                title: 'Что-то пошло не так:(',
                message: 'Чтобы связаться нажмите тут',
                url: 'mailto:me@vldsx.com',
                targer: '_blank'
            }, {
                type: 'danger'
            });
        }).fail(function () {
            $.notify({
                title: 'Что-то пошло не так:(',
                message: 'Чтобы связаться нажмите тут',
                url: 'mailto:me@vldsx.com',
                targer: '_blank'
            }, {
                type: 'danger'
            });
        });
    }

    $(document).ready(function(){
        $('form.js-form').each(function () {
            new pageFormProcessor(this);
        });
    });
})();
