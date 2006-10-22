# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: decorators.py 11 2006-10-22 10:03:27Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/decorators.py $
# $LastChangedDate: 2006-10-22 11:03:27 +0100 (Sun, 22 Oct 2006) $
#             $Rev: 11 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import pylons
import formencode.api as api
import formencode.variabledecode as variabledecode

from pylons.decorator import decorator
from pylons import c
from pylons.templating import render_response

def validate(template=None, schema=None, validators=None, form=None,
             variable_decode=False, dict_char='.', list_char='-',
             post_only=True):
    """Validate input either for a FormEncode schema, or individual validators

    Given a form schema or dict of validators, validate will attempt to validate
    the schema or validator list as long as a POST request is made. No 
    validation is performed on GET requests.

    If validation was succesfull, the valid result dict will be saved
    as ``self.form_result``. Otherwise, the action will be re-run as if it was a
    GET, and the output will be filled by FormEncode's htmlfill to fill in the
    form field errors.

    If you'd like validate to also check GET (query) variables during its 
    validation, set the ``post_only`` keyword argument to False.

    Example:

    .. code-block:: Python

        class SomeController(BaseController):

            def index(self, id):
                return render_response('template')

            # If request.method == POST run update_post
            @rest.dispatch_on(POST='update_post')
            def update(self):
                return render_response('template.update')

            @validate(schema=model.forms.myshema(), form='update')
            def update_post(self):
                # Do what you want with the request.POST vars passed from form
                # Finnaly issue a redirect_to because in case a user tries to
                # reload, it won't try to submit form again
                return redirect_to(action='index')

    """
    def wrapper(func, self, *args, **kwargs):
        """Decorator Wrapper function"""
        defaults, errors = {}, {}
        if not pylons.request.method == 'POST':
            return func(self, *args, **kwargs)
        if post_only:
            postvars = pylons.request.POST.copy()
        else:
            postvars = pylons.request.params.copy()
        if variable_decode:
            postvars = variabledecode.variable_decode(postvars, dict_char,
                                                      list_char)

        defaults.update(postvars)
        if schema:
            try:
                self.form_result = schema.to_python(defaults)
            except api.Invalid, e:
                errors = e.unpack_errors(variable_decode, dict_char, list_char)
        if validators:
            if isinstance(validators, dict):
                if not hasattr(self, 'form_result'):
                    self.form_result = {}
                for field, validator in validators.iteritems():
                    try:
                        self.form_result[field] = \
                            validator.to_python(defaults[field] or None)
                    except api.Invalid, error:
                        errors[field] = error
        if errors:
            c.form_errors = errors
            c.form_result = defaults
            return render_response(template)
        return func(self, *args, **kwargs)
    return decorator(wrapper)


