/* -*- coding: utf-8 -*-
 * vim: sw=4 ts=4 fenc=utf-8
 * =============================================================================
 * $Id: ispmanccp.js 5 2006-09-01 19:30:14Z s0undt3ch $
 * =============================================================================
 *             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/public/js/ispmanccp.js $
 * $LastChangedDate: 2006-09-01 20:30:14 +0100 (Fri, 01 Sep 2006) $
 *             $Rev: 5 $
 *   $LastChangedBy: s0undt3ch $
 * =============================================================================
 * Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
 *
 * Please view LICENSE for additional licensing information.
 * =============================================================================
*/

var myimages=new Array()
function preloadimages(){
    for (i=0;i<preloadimages.arguments.length;i++){
        myimages[i]=new Image()
        myimages[i].src=preloadimages.arguments[i]
    }
}
preloadimages("/images/logo.jpg","/images/loading.gif");
