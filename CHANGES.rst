Changelog
=========

1.3 (unreleased)
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
