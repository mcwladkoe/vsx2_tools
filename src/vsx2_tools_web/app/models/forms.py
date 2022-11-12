from PIL import ImageColor
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, SelectField, StringField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import ColorInput

from vsx2_change_layout import get_all_layouts


ALL_LAYOUTS = get_all_layouts()


class FormWithInputField(FlaskForm):
    input_ = TextAreaField(validators=[DataRequired(), Length(min=1, max=10_000)])


class LayoutForm(FormWithInputField):
    source = SelectField(
        choices=[
            (layout, " ".join(layout.split("_")).upper()) for layout in ALL_LAYOUTS
        ],
        validators=[DataRequired()],
        default='ru_qwerty'
    )
    destination = SelectField(
        choices=[
            (layout, " ".join(layout.split("_")).upper()) for layout in ALL_LAYOUTS
        ],
        validators=[DataRequired()],
        default='ua_qwerty'
    )


class StrikethroughForm(FormWithInputField):
    pass


class RotateForm(FormWithInputField):
    pass


class ColorField(StringField):
    widget = ColorInput()

    error_msg = "Not a valid color."

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data:
            return str(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        if valuelist:
            if not valuelist[0]:
                self.data = None
            else:
                try:
                    self.data = ImageColor.getcolor(valuelist[0], "RGB")
                except AttributeError:
                    self.data = None
                    raise ValueError(self.gettext(self.error_msg))


class MemeGeneratorForm(FlaskForm):
    text = StringField(validators=[DataRequired(), Length(min=1, max=10_000)])
    text_color = ColorField()
    image = FileField(validators=[FileRequired(), FileAllowed(["png", "jpg"], "wrong format!")])
