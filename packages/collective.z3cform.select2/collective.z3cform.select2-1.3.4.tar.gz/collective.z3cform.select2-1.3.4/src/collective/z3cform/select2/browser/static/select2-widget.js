var initializeSelect2SingleWidget = function(obj, width) {
  if (typeof width === "undefined") {
      width = 'resolve';
  }

  var format = function(state) {
      var option = $(state.element);
      return '<span class="' + option.data('css') + '">' + state.text + '</span>';
  };

  jQuery(obj).select2({
      width: width,
      formatResult: format,
      formatSelection: format,
      escapeMarkup: function(m) { return m; }
  });
};

initializeSelect2Widgets = function(width) {
  if (typeof width === "undefined") {
      width = 'resolve';
  }

  jQuery('.single-select2-widget').each(function() {
    initializeSelect2SingleWidget($(this), width=width);
  });

};

jQuery(document).ready(initializeSelect2Widgets);
