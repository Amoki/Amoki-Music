/* global define */
function setupKoBootstrap(koObject, $) {
  "use strict";
  // Outer HTML
  if(!$.fn.outerHtml) {
    $.fn.outerHtml = function() {
      if(this.length === 0) {
        return false;
      }
      var elem = this[0];
      var name = elem.tagName.toLowerCase();
      if(elem.outerHTML) {
        return elem.outerHTML;
      }
      var attrs = $.map(elem.attributes, function(i) {
        return i.name + '="' + i.value + '"';
      });
      return "<" + name + (attrs.length > 0 ? " " + attrs.join(" ") : "") + ">" + elem.innerHTML + "</" + name + ">";
    };
  }

  // Bind Bootstrap Popover
  koObject.bindingHandlers.popover = {
    init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
      var $element = $(element);
      var popoverBindingValues = koObject.utils.unwrapObservable(valueAccessor());
      var template = popoverBindingValues.template || false;
      var options = popoverBindingValues.options || {title: 'popover'};
      var data = popoverBindingValues.data || false;
      var controlDescendants = popoverBindingValues.controlDescendants;
      if(template !== false) {
        if(data) {
          options.content = "<!-- ko template: { name: template, if: data, data: data } --><!-- /ko -->";
        }
        else {
          options.content = $('#' + template).html();
        }
        options.html = true;
      }
      $element.on('shown.bs.popover', function(event) {

        var popoverData = $(event.target).data();
        var popoverEl = popoverData['bs.popover'].$tip;
        var options = popoverData['bs.popover'].options || {};
        var button = $(event.target);
        var buttonPosition = button.position();
        var buttonDimensions = {
          x: button.outerWidth(),
          y: button.outerHeight()
        };


        koObject.cleanNode(popoverEl[0]);
        if(data) {
          ko.applyBindings({template: template, data: data}, popoverEl[0]);
        }
        else {
          var childBindingContext = bindingContext.createChildContext(
            bindingContext.$rawData,
            null, // Optionally, pass a string here as an alias for the data item in descendant contexts
            function(context) {
              ko.utils.extend(context, valueAccessor());
            }
          );
          ko.applyBindings(childBindingContext, popoverEl[0]);
        }

        var popoverDimensions = {
          x: popoverEl.outerWidth(),
          y: popoverEl.outerHeight()
        };

        popoverEl.find('button[data-dismiss="popover"]').click(function() {
          button.popover('hide');
        });

        switch (options.placement) {
          case 'right':
            popoverEl.css({
              left: buttonDimensions.x + buttonPosition.left,
              top: (buttonDimensions.y / 2 + buttonPosition.top) - popoverDimensions.y / 2
            });
          break;
          case 'left':
            popoverEl.css({
              left: buttonPosition.left - popoverDimensions.x,
              top: (buttonDimensions.y / 2 + buttonPosition.top) - popoverDimensions.y / 2
            });
          break;
          case 'top':
            popoverEl.css({
              left: buttonPosition.left + (buttonDimensions.x / 2 - popoverDimensions.x / 2),
              top: buttonPosition.top - popoverDimensions.y
            });
          break;
          case 'bottom':
            popoverEl.css({
              left: buttonPosition.left + (buttonDimensions.x / 2 - popoverDimensions.x / 2),
              top: buttonPosition.top + buttonDimensions.y
            });
          break;
        }
      });

      $element.popover(options);
      koObject.utils.domNodeDisposal.addDisposeCallback(element, function() {
        $element.popover('destroy');
      });

      return {controlsDescendantBindings: typeof controlDescendants === 'undefined' ? true : controlDescendants};

    }
  };

}

(function(factory) {
  "use strict";
  // Support multiple loading scenarios
  if(typeof define === 'function' && define.amd) {
    // AMD anonymous module

    define(["require", "exports", "knockout", "jquery"], function(require, exports, knockout, jQuery) {
      factory(knockout, jQuery);
    });
  }
  else {
    // No module loader (plain <script> tag) - put directly in global namespace
    factory(window.ko, jQuery);
  }
}(setupKoBootstrap));
