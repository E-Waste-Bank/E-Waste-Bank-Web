from django.urls import path
from about_us.views import show_about_us, get_feedback_json, add_feedback#, show_json_by_id

urlpatterns = [
    path('', show_about_us, name='show_about_us'),
    path('add-feedback/', add_feedback, name='add_feedback'),
    path('get-latest-three/', get_feedback_json, name='get_feedback_json'),
    #path('json/<int:id>', show_json_by_id, name='show_json_by_id'),
]