Changelog
=========

All notable changes to HTTPolice will be documented in this file.

This project adheres to `Semantic Versioning <http://semver.org/>`_
(which means it is unstable until 1.0).


0.4.0 - 2017-01-14
~~~~~~~~~~~~~~~~~~

Added
-----
- Python 3.6 compatibility.
- Decompression of `brotli`_ compressed payloads (``Content-Encoding: br``).
- Checks for JSON charsets (notices `1280`_ and `1281`_).
- Checks for some wrong media types,
  currently ``plain/text`` and ``text/json`` (notice `1282`_).

.. _brotli: https://tools.ietf.org/html/rfc7932
.. _1280: http://pythonhosted.org/HTTPolice/notices.html#1280
.. _1281: http://pythonhosted.org/HTTPolice/notices.html#1281
.. _1282: http://pythonhosted.org/HTTPolice/notices.html#1282

Removed
-------
- The deprecated constants
  ``httpolice.ERROR``, ``httpolice.COMMENT``, ``httpolice.DEBUG``
  have been removed. Use ``httpolice.Severity`` instead.
- When checking XML payloads, HTTPolice
  no longer takes precautions against denial-of-service attacks,
  because the `defusedxml`_ module does not currently work with Python 3.6.
  DoS attacks against HTTPolice are considered unlikely and non-critical.
- Notice 1275 ("XML with entity declarations") has been removed
  for the same reason.

.. _defusedxml: https://pypi.python.org/pypi/defusedxml/

Other
-----
- There is now a third-party `Chrome extension`_ for HTTPolice.

.. _Chrome extension: https://chrome.google.com/webstore/detail/httpolice-devtool/hnlnhebgfcfemjaphgbeokdnfpgbnhgn


0.3.0 - 2016-08-14
~~~~~~~~~~~~~~~~~~

Added
-----
- HTTPolice now caches more intermediate values in memory,
  which makes it significantly faster in many cases.
- HTTPolice now works correctly under `PyPy`_ (the 2.7 variant),
  which, too, can make it faster on large inputs.
  You will probably need a recent version of PyPy (5.3.1 is OK).
- `HTML reports`_ now have an "options" menu
  to filter exchanges and notices on the fly.
- The ``httpolice`` command-line tool now has
  a ``--fail-on`` option to exit with a non-zero status
  if any notices with a given severity have been reported.
- Work around various problems in HAR files exported by Firefox and `Fiddler`_.
- HTML reports can now display a remark before every request and response
  (enabled with the *Show remarks* checkbox in the "options" menu).
  The ``httpolice`` command-line tool puts the input filename in this remark.
  With the `Python API`_, you can put anything there
  using the ``remark`` argument to ``Request`` and ``Response`` constructors.
- Notices about HTTP/1.x framing errors (such as `1006`_)
  now include the input filename as well.
- Check for missing scheme name in authorization headers (notice `1274`_).
- Check for missing quality values in headers like Accept (notice `1276`_).
- Check for obsolete 'X-' prefix in experimental headers (notice `1277`_).
- Notice `1093`_ recognizes a few more product names as client libraries.

.. _HTML reports: http://httpolice.readthedocs.io/en/stable/reports.html
.. _Fiddler: http://www.telerik.com/fiddler
.. _PyPy: http://pypy.org/
.. _Python API: http://httpolice.readthedocs.io/en/stable/api.html
.. _1006: http://pythonhosted.org/HTTPolice/notices.html#1006
.. _1093: http://pythonhosted.org/HTTPolice/notices.html#1093
.. _1274: http://pythonhosted.org/HTTPolice/notices.html#1274
.. _1276: http://pythonhosted.org/HTTPolice/notices.html#1276
.. _1277: http://pythonhosted.org/HTTPolice/notices.html#1277

Changed
-------
- For the `tcpick and tcpflow input`_ modes,
  you now have to use different options to tcpick/tcpflow (consult the manual).
- `Text reports`_ no longer show request/response numbers.
  If you parse these reports, you may need to adjust.
- Styles in HTML reports have been tweaked to make them more readable.

.. _Text reports: http://httpolice.readthedocs.io/en/stable/reports.html
.. _tcpick and tcpflow input:
   http://httpolice.readthedocs.io/en/stable/streams.html

Deprecated
----------
- In the `Python API`_,
  the constants ``httpolice.ERROR``, ``httpolice.COMMENT``, ``httpolice.DEBUG``
  have been replaced with a single ``httpolice.Severity`` enumeration,
  and will be removed in the next release.

.. _Python API: http://httpolice.readthedocs.io/en/stable/api.html

Fixed
-----
- The `tcpick and tcpflow input`_ modes should now be more reliable,
  although they still suffer from certain problems.
- CONNECT requests in HAR files are now handled correctly.
- Notices `1053`_ and `1066`_ are no longer reported
  on requests with bodies of length 0.

.. _tcpick and tcpflow input:
   http://httpolice.readthedocs.io/en/stable/streams.html
.. _1053: http://pythonhosted.org/HTTPolice/notices.html#1053
.. _1066: http://pythonhosted.org/HTTPolice/notices.html#1066


0.2.0 - 2016-05-08
~~~~~~~~~~~~~~~~~~

Added
-----
- `Django integration`_ (as a separate distribution).
- Unwanted notices can now be `silenced`_.
- Checks for OAuth `bearer tokens`_.
- Checks for the `Content-Disposition`_ header.
- Checks for `RFC 5987`_ encoded values.
- Checks for `alternative services`_.
- Checks for HTTP/1.1 connection control features `prohibited in HTTP/2`_.
- `Stale controls`_ are now recognized.
- Checks for status code `451 (Unavailable For Legal Reasons)`_.

.. _Django integration: http://httpolice.readthedocs.io/en/stable/django.html
.. _silenced: http://httpolice.readthedocs.io/en/stable/concepts.html#silence
.. _bearer tokens: http://tools.ietf.org/html/rfc6750
.. _Content-Disposition: http://tools.ietf.org/html/rfc6266
.. _RFC 5987: https://tools.ietf.org/html/rfc5987
.. _alternative services: https://tools.ietf.org/html/rfc7838
.. _prohibited in HTTP/2: https://tools.ietf.org/html/rfc7540#section-8.1.2.2
.. _Stale controls: https://tools.ietf.org/html/rfc5861
.. _451 (Unavailable For Legal Reasons): https://tools.ietf.org/html/rfc7725

Changed
-------
- `mitmproxy integration`_ has been moved into a separate distribution.

.. _mitmproxy integration:
   http://httpolice.readthedocs.io/en/stable/mitmproxy.html

Fixed
-----
- Input files from tcpick are sorted correctly.
- Notice `1108`_ doesn't crash in non-English locales.
- Notices such as `1038`_ are not reported on responses to HEAD.

.. _1108: http://pythonhosted.org/HTTPolice/notices.html#1108
.. _1038: http://pythonhosted.org/HTTPolice/notices.html#1038


0.1.0 - 2016-04-25
~~~~~~~~~~~~~~~~~~

- Initial release.
