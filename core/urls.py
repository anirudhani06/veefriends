import debug_toolbar
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("posts.urls")),
    path('user/', include("accounts.urls")),
    path('chat/', include("chat.urls")),
    path('__debug__/', include(debug_toolbar.urls)),
]


urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)