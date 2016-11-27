var tabsFn = (function() {

  function init() {
    setHeight();
  }

  function setHeight() {
    var $tabPane = $('.tab-pane'),
        tabsHeight = $('.nav-tabs').height();

    $tabPane.css({
      height: tabsHeight
    });
  }

  $(init);
})();/**
 * Created by admin on 27.11.2016.
 */
