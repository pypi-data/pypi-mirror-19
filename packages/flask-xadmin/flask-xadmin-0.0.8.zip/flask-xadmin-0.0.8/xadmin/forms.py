# -*- coding: utf-8 -*-
from flask_security.forms import Form,LoginForm
from wtforms import SubmitField, PasswordField,HiddenField,validators
from wtforms.validators import Required
from flask_security.utils import verify_and_update_password
from flask_security import current_user


#Form to enter edit mode
class EditModeForm(Form):
    password = password = PasswordField(u'Password')
    next = HiddenField()
    submit = SubmitField(u'Potvrdi')

    def validate(self):
        if not Form.validate(self):
            return False

        if self.password.data.strip() == '':
            self.password.errors.append(u'Niste unijeli lozinku')
            return False

        if not verify_and_update_password(self.password.data, current_user):
            self.password.errors.append(u'Pogrešna lozinka')
            return False

        return True

