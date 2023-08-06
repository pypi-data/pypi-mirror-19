Changelog
=========

0.7 (2017-01-23)
----------------

- Use `category_uid` instead `category_id` as key for infos dict used by
  `CategorizedChildInfosView`, indeed we may have different configurations
  used on same container for different categorized elements and those
  configurations may contain categories with same id
  [gbastien]
- Do not break if icon used for iconified category contains special characters
  [gbastien]

0.6 (2017-01-17)
----------------

- Use ajax to display the categorized childs informations
  [gbastien]
- Display select2 widget larger and with no padding between options
  so more options are displayed together
  [gbastien]
- Added option `show_nothing=True` to the `categorized-childs` view
  to be able to show/hide the 'Nothing' label when there is no categorized
  content to display
  [gbastien]

0.5 (2017-01-13)
----------------

- Do not fail in `utils.sort_categorized_elements` if a key is not found,
  it can be the case when copy/pasting and new element use another
  configuration
  [gbastien]

0.4 (2017-01-12)
----------------

- Sort `categorized_elements` by alphabetical order into a category,
  this way it can be directly displayed as it in the tooltipster
  or in the tabview without having to sort elements again
  [gbastien]
- Add method `IconifiedCategoryGroupAdapter.get_every_categories`
  that gets every available categories.  Mainly made to be overrided,
  it is used in `utils.get_ordered_categories` to manage the fact
  that a container could contain categorized elements using different
  group of categories
  [gbastien]
- Add a configlet to allow user to sort elements on title on the
  categorized tab view
  [mpeeters]
- Ensure that categorized elements are sorted by group folder order
  [mpeeters]
- Refactoring of iconified JavaScript functions
  [mpeeters]
- Increase speed that show the categorized elements in the tooltipster.
  [gbastien]
- Do not fail to remove the Plone Site if categories or subcategorie exist.
  [gbastien]

0.3 (2016-12-21)
----------------

- Changed icon used with link to `More infos`.
  [gbastien]
- Do not fail if subcategory title contains special characters.
  [gbastien]
- Turn icon `more_infos.png` into a separated resource, in addition to other
  resources stored in the `static` folder declared as resourceDirectory,
  so it is easy to override.
  [gbastien]

0.2 (2016-12-07)
----------------

- Use `javascript:event.preventDefault()` when clicking on the tooltipster root
  element to avoid the link action that will change the current url.
  [gbastien]
- Open `More infos` link in `target=_parent` so it opens in the _parent frame
  when displayed in an iframe, namely outside the iframe.
  [gbastien]

0.1 (2016-12-02)
----------------

- Initial release.
  [mpeeters]
