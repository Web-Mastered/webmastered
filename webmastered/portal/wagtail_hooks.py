from wagtail.admin.views.account import BaseSettingsPanel
from wagtail.core import hooks

from .forms import CustomStaffSettingsForm

@hooks.register('register_account_settings_panel')
class CustomStaffSettingsPanel(BaseSettingsPanel):
    name = 'custom_staff'
    title = "Staff settings"
    order = 300
    form_class = CustomStaffSettingsForm
    form_object = 'profile'

    def get_form(self):
        """
        Returns an initialised form.
        """
        kwargs = {
            'instance': self.request.user.staff_profile,
            'prefix': self.name
        }

        if self.request.method == 'POST':
            return self.form_class(self.request.POST, **kwargs)
        else:
            return self.form_class(**kwargs)

