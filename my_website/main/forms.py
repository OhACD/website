from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full name'}))
    mailing_list = forms.BooleanField(required=False, initial=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ['email', 'name', 'mailing_list']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_input = "w-full rounded-xl border border-brand-baseMuted bg-brand-base px-4 py-3 text-brand-text placeholder-brand-textMuted focus:border-brand-accentMint focus:outline-none focus:ring-2 focus:ring-brand-accentMint/50"
        checkbox = "h-4 w-4 rounded border-brand-baseMuted text-brand-accentMint focus:ring-brand-accentMint/60"
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = f"{widget.attrs.get('class', '')} {checkbox}".strip()
            else:
                widget.attrs['class'] = f"{widget.attrs.get('class', '')} {base_input}".strip()
                widget.attrs.setdefault('placeholder', field.label)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error("password2", "Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
