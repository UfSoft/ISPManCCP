# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: helpers.py 4 2006-08-28 14:00:08Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/helpers.py $
# $LastChangedDate: 2006-08-28 15:00:08 +0100 (Mon, 28 Aug 2006) $
#             $Rev: 4 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

"""
Helper functions

All names available in this module will be available under the Pylons h object.
"""
from webhelpers import *
from datetime import date


def date_from_tstamp(tstamp):
    return date.fromtimestamp(int(tstamp))
