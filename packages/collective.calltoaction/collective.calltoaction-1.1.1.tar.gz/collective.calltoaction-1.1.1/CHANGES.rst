Changelog
=========


1.1.1 (2017-02-08)
------------------

- Fixed problem when showing viewlet with form globally.
  After submit, the form could then be shown twice.
  We had already fixed that for the normal case,
  but not for the case where the viewlet is globally shown.
  [maurits]


1.1 (2017-02-07)
----------------

- Added form field to portlet.  You can select a PloneFormGen FormFolder with this.
  The portlet then shows this as an embedded form under the title and text.
  [maurits]

- Added control panel option to always show the popup.
  This ignores the cookie. This can be handy during development.
  You need to run the upgrade in the add-ons control panel.
  [maurits]


1.0 (2016-11-01)
----------------

- Added option to show action globally, regardless of blocked portlets.
  The timeout is now always the time since the first visit of a page with this portlet.
  [maurits]


1.0rc1 (2016-04-20)
-------------------

- Set overlay fixed and center of the browser.


1.0b3 (2016-04-13)
------------------

- Except AttributeErrors only, and verify if an image is actually
  uploaded to a newsitem.  [jladage]


1.0b2 (2016-04-13)
------------------

- Support both ATImage and ATNewsItem as providers of images.
  [jladage]


1.0b1 (2016-04-06)
------------------

- Initial release.
  [mauritsvanrees]
