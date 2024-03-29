/*
 * rest-prefs.js
 *
 * Marginalia has been developed with funding and support from
 * BC Campus, Simon Fraser University, and the Government of
 * Canada, and units and individuals within those organizations.
 * Many thanks to all of them.  See CREDITS.html for details.
 * Copyright (C) 2005-2007 Geoffrey Glass www.geof.net
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */

NICE_PREFERENCE_SERVICE_URL = '/preference';
UGLY_PREFERENCE_SERVICE_URL = '/preference';

function RestPreferenceService( wwwroot )
{
	this.wwwroot = wwwroot;
	return this;
}

/**
 * Fetch all preferences for the current user
 * There is little point in implementing methods to fetch individual preferences,
 * because the call is asynchronous.  Instead, the preference service should
 * cache the results.
 */
RestPreferenceService.prototype.listPreferences = function( f )
{
	var serviceUrl;
	if ( ANNOTATION_NICE_URLS )
		serviceUrl = this.wwwroot + NICE_PREFERENCE_SERVICE_URL;
	else
		serviceUrl = this.wwwroot + UGLY_PREFERENCE_SERVICE_URL;	
	
	var xmlhttp = createAjaxRequest( );
	xmlhttp.open( 'GET', serviceUrl, true );
	xmlhttp.onreadystatechange = function( ) {
		if ( xmlhttp.readyState == 4 )
		{
			if ( 200 == xmlhttp.status )
			{
				if ( null != f )
					f( xmlhttp.responseText );
			}
			else
				alert( "serverGetPreference failed with code " + xmlhttp.status + "\n" + xmlhttp.responseText );
		}
	}
	//trace( "PreferenceService.setPreference " + serviceUrl)
	xmlhttp.send( null );
}

RestPreferenceService.prototype.setPreference = function( setting, value, f )
{
	var serviceUrl;
	if ( ANNOTATION_NICE_URLS )
		serviceUrl = this.wwwroot + NICE_PREFERENCE_SERVICE_URL + '?name=' + encodeURIComponent( setting );
	else
		serviceUrl = this.wwwroot + UGLY_PREFERENCE_SERVICE_URL + '?name=' + encodeURIComponent( setting );

	var body = 'value=' + encodeURIComponent( value );
	var xmlhttp = createAjaxRequest( );
	xmlhttp.open( 'POST', serviceUrl, true );
	xmlhttp.setRequestHeader( 'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8' );
	xmlhttp.setRequestHeader( 'Content-length', body.length );
	xmlhttp.onreadystatechange = function( ) {
		if ( xmlhttp.readyState == 4 )
		{
			// Safari is braindead here:  any status code other than 200 is converted to undefined
			// IE invents its own 1223 status code
			// See http://www.trachtenberg.com/blog/?p=74
			if ( 204 == xmlhttp.status || null == xmlhttp.status || 1223 == xmlhttp.status )
			{
				if ( null != f )
					f( );
			}
			else
				alert( "serverSetPreference failed with code " + xmlhttp.status + "\n" + xmlhttp.responseText );
		}
	}
	//trace( "PreferenceService.setPreference " + serviceUrl)
	xmlhttp.send( body );
}
