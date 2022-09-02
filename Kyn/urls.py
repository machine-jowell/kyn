"""Kyn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from main.views import (
    homepage,
    aboutus,
    faq,
    register,
    login_user,
    logout_user,
    view_profile,
    edit_profile,
    view_profile_events,
    create_event,
    view_event,
    edit_event,
    remove_event,
    participate_event,
    remove_participation_event,
    event_list_view,
    change_password,

)

from .views import (
    eventList,
    eventDetail,
    eventCreate,
)

urlpatterns = [
    # homepage, register, login, logout
    path("", homepage, name="home"),
    path("aboutus/", aboutus, name="aboutus"),
    path("faq/", faq, name="faq"),
    path('register/', register, name="register"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),

    # profile
    path('profile/', view_profile, name="profile"),
    path('edit/', edit_profile, name="editProfile"),
    path('editPassword/', change_password, name="changePassword"),
    path('profileEvents/', view_profile_events, name="profileEvents"),

    # events
    path('create_event/', create_event, name="createEvent"),
    path('view_event/<int:id>/', view_event, name="viewEvent"),
    path('edit_event/<int:id>', edit_event, name="editEvent"),
    path('remove_event/<int:id>/', remove_event, name="removeEvent"),
    path('participate/<int:id>/', participate_event, name='participate'),
    path('remove_participation/<int:id>/', remove_participation_event, name="removeParticipation"),
    path('eventlist/', event_list_view, name="eventList"),

    # REST API
    path('api/event-list', eventList, name="api-eventList"),
    path('api/event/<int:id>', eventDetail, name="api-eventDetail"),
    path('api/event-create/', eventCreate, name="api-eventCreate"),


    # admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
