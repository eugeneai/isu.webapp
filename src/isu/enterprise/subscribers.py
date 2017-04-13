from pyramid.renderers import get_renderer

#from pyramid.events import subscriber, BeforeRender


#@subscriber(BeforeRender)
def add_base_template(event):
    """Add base templates.
    """
    main = get_renderer('templates/index.pt').implementation()
    test = get_renderer('templates/main.pt').implementation()
    #email_main = get_renderer('templates/email/main.pt').implementation()
    email_main = False
    event.update({'main': main, 'test': test, 'email_main': email_main})
