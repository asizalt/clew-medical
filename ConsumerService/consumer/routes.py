from views import  events,event_by_patient,event_patient_medication

def setup_routes(app):
    app.router.add_get('/api/events', events, name='events')
    app.router.add_get('/api/patient/{id}', event_by_patient, name='event_by_patient')
    app.router.add_get('/api/patient/{patient_id}/medication/{medication_id}', event_patient_medication, name='event_patient_medication')

# routes = [
#     # ('POST', '/api/v1/users/registration/', views.registration),
#     # ('POST', '/api/v1/users/login/', views.login),
#     ('GET', '/api/events', views.all_events),
#     ('GET', r'/api/events/patient/{id:\d+}/', views.event_by_patient),
#     # ('GET', r'/api/v1/status/{id:\d+}/', views.all_event_status),
#     # ('GET', r'/api/v1/status/{id:\d+}/', views.all_event_status),
#     # ('POST', '/api/v1/jokes/', views.joke_create),
#     # ('GET', r'/api/v1/jokes/{id:\d+}/', views.joke_detail),
#     # ('PATCH', r'/api/v1/jokes/{id:\d+}/', views.joke_update),
#     # ('DELETE', r'/api/v1/jokes/{id:\d+}/', views.joke_delete),
# ]
