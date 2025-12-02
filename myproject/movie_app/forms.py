from django import forms
from django.contrib.auth.models import User
from .models import WatchHistory, Movie


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Birthday")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class AddMovieForm(forms.ModelForm):
    watch_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    rating = forms.FloatField(min_value=0.1, max_value=10, label="Your Rating (0.1-10)")
    review = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        label="Review",
        required=False
    )
    
    class Meta:
        model = WatchHistory
        fields = ['movie', 'watch_date', 'rating', 'review']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate movie queryset at form initialization
        self.fields['movie'] = forms.ModelChoiceField(
            queryset=Movie.objects.all().order_by('title'),
            label="Select Movie",
            help_text="Choose a movie from the database",
            empty_label="-- Select a Movie --"
        )