from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .routers import router
from accounts.views import *



urlpatterns = [
    path('staff/logout/', custom_logout, name='logout'),
    path('staff/', admin.site.urls, name='admin_login'),
    path('', include('accounts.urls')),
    # path('payments/', include('payments.urls')),
    path('', include('core.urls', namespace='core')),
    path('api/', include(router.urls)),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
