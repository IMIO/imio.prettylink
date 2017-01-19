Changelog
=========

1.5 (unreleased)
----------------

- Added submethod _get_url that does the url computation.
  Additionally it manages the fact that context is a Dexterity file and
  append relevant part to the url (/@@download/...).
  [gbastien]
- Do not break if icon name contains special characters.
  [gbastien]

1.4 (2016-08-17)
----------------

- Added CSS class 'no_access' to <span> "can_not_access_this_element"
  in addition to class 'discreet' so it may be customized if necessary.
  [gbastien]
- Initialize the 'title' attribute with contentValue, this way if a
  content is cropped to be displayed (maxLength=...), the complete content
  is displayed on hover.
  [gbastien]

1.3 (2016-04-20)
----------------

- Make sure quotes used in title are not breaking formatted strings,
  we escape it by replacing quotes by it's HTML entity &#39;
  [gbastien]

1.2 (2016-02-16)
----------------

- If 'isViewable' is True (default), check that current user have
  'View' on the linked element, if it is forced to False, leave it False.
  This way, 'View' check to linked element is managed by imio.prettylink.
  [gbastien]

1.1 (2015-11-13)
----------------

- When using 'showColors', do not fail if element has no workflow.
  [gbastien]
- Makes 'showContentIcon' work, fixed several bugs.
  [gbastien] 

1.0 (2015-07-14)
----------------

- Initial release.
  [gbastien]
