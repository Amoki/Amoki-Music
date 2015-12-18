var sortableOptions = {
  axis: "y",
  revert: true,
  cursor: "move",
  scrollSpeed: 5,
  delay: 150,
  over: function() {
    $(this).find('.ui-sortable-helper').appendTo(this);
  },
};

var afterMoveSortable = function(obj) {
  var action = "";
  var targetPk;
  if(obj.targetIndex < obj.sourceParent().length - 1) {
    action = "above";
    targetPk = obj.sourceParent()[obj.targetIndex + 1].pk();
  }
  else {
    action = "below";
    targetPk = obj.sourceParent()[obj.targetIndex - 1].pk();
  }
  roomVM.postPlaylistSort(obj.item.pk(), action, targetPk);
};

ko.bindingHandlers.stopBinding = {
  init: function() {
    return {controlsDescendantBindings: true};
  }
};
ko.virtualElements.allowedBindings.stopBinding = true;

ko.bindingHandlers.selectPicker = {
  init: function(element, valueAccessor, allBindingsAccessor) {
    if($(element).is('select')) {
      if(ko.isObservable(valueAccessor())) {
        if($(element).prop('multiple') && $.isArray(ko.utils.unwrapObservable(valueAccessor()))) {
          // in the case of a multiple select where the valueAccessor() is an observableArray, call the default Knockout selectedOptions binding
          ko.bindingHandlers.selectedOptions.init(element, valueAccessor, allBindingsAccessor);
        }
        else {
          // regular select and observable so call the default value binding
          ko.bindingHandlers.value.init(element, valueAccessor, allBindingsAccessor);
        }
      }
      $(element).addClass('selectpicker').selectpicker();
    }
  },
  update: function(element, valueAccessor, allBindingsAccessor) {
    if($(element).is('select')) {
      var selectPickerOptions = allBindingsAccessor().selectPickerOptions;
      if(typeof selectPickerOptions !== 'undefined' && selectPickerOptions !== null) {
        var options = selectPickerOptions.optionsArray;
        var isDisabled = selectPickerOptions.disabledCondition || false;
        var resetOnDisabled = selectPickerOptions.resetOnDisabled || false;
        if(ko.utils.unwrapObservable(options).length > 0) {
          // call the default Knockout options binding
          ko.bindingHandlers.options.update(element, options, allBindingsAccessor);
        }
        if(isDisabled && resetOnDisabled) {
          // the dropdown is disabled and we need to reset it to its first option
          $(element).selectpicker('val', $(element).children('option:first').val());
        }
        $(element).prop('disabled', isDisabled);
      }
      if(ko.isObservable(valueAccessor())) {
        if($(element).prop('multiple') && $.isArray(ko.utils.unwrapObservable(valueAccessor()))) {
          // in the case of a multiple select where the valueAccessor() is an observableArray, call the default Knockout selectedOptions binding
          ko.bindingHandlers.selectedOptions.update(element, valueAccessor);
        }
        else {
          // call the default Knockout value binding
          ko.bindingHandlers.value.update(element, valueAccessor);
        }
      }

      $(element).selectpicker('refresh');
    }
  }
};

ko.subscribable.fn.trimmed = function() {
  return ko.computed({
    read: function() {
      if(this()) {
        return this().trim();
      }
    },
    write: function(value) {
      if(value) {
        this(value.trim());
      }
      else {
        this(null);
      }
      this.valueHasMutated();
    },
    owner: this
  });
};

ko.bindingHandlers.visibleKeepDOM = {
  init: function(element) {
    $(element).children().each(function() {
      $(this).hide();
    });
  },
  update: function(element, valueAccessor) {
    values = ko.unwrap(valueAccessor());
    if(values) {
      $(element).children('.' + values.source()).show();
    }
    else {
      $(element).children().each(function() {
        $(this).fadeOut(1000);
      });
    }
  }
};
