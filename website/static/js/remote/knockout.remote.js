// MODEL DEFINITION
// Music model
function Music(data) {
  this.musicId = ko.observable(data.music_id);
  this.name = ko.observable(data.name);
  url = ko.observable(data.url);
  room = ko.observable(data.room);
  date = ko.observable(data.date);
  this.duration = ko.observable(data.duration);
  this.thumbnail = ko.observable(data.thumbnail);
  this.count = ko.observable(data.count);
  lastPlay = ko.observable(data.last_play);
  deadLink = ko.observable(data.dead_link);
  timerStart = ko.observable(data.timer_start);
  timerEnd = ko.observable(data.timer_end);
  source = ko.observable(data.source);
}
// Source model
function Source(data) {
  this.name = ko.observable(data.name);
}

// VIEW MODEL DEFINITION
// Library view model
function LibraryViewModel() {
  var self = this;

  self.sourceSearch = ko.observable();
  self.querySearch = ko.observable();

  // library part
  self.musicsLibrary = ko.observableArray([]);
  self.hasPrevious = ko.observable();
  self.hasNext = ko.observable();
  self.currentPage = ko.observable();

  // search part
  self.musicSearch = ko.observableArray([]);

  // TEST ONLY
  self.sources = ko.observableArray([
      new Source({name: "Soundcloud test"}),
      new Source({name: "Youtube test"}),
    ]);

  self.addMusic = function() {
    // endpointAddMusic(Music);
    console.log(ko.toJSON(this));
  };

  self.searchMusic = function() {
    // Return a json serialized Music object
    $.getJSON("/search",
      {
        "source": ko.toJSON(self.sourceSearch),
        "q": ko.toJSON(self.querySearch)
      },
      function(allData) {
        var mappedMusics = $.map(allData, function(item) {
          return new Music(item);
        });
        self.musicSearch(mappedMusics);
      }).fail(function(jqxhr) {
        console.error(jqxhr.responseText);
      });
  };

  // Load Library page from server, convert it to Music instances, then populate self.musics
  self.getLibrary = function() {
    $.getJSON("/musics/", function(allData) {
      var mappedMusics = $.map(allData, function(item) {
        return new Music(item);
      });
      self.musicsLibrary(mappedMusics);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  // Load Sources from server, convert it to Source instances, then populate self.sources
  self.getSources = function() {
    $.getJSON("/sources", function(allData) {
      var mappedSources = $.map(allData, function(item) {
        return new Source(item);
      });
      self.sources(mappedSources);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };
}

// Playist view model
function PlaylistViewModel() {
  var self = this;
  self.musics = ko.observableArray([]);

  self.addMusic = function(music) {
    endpointAddMusic(music);
  };
  self.removeMusic = function(music) {
    self.musics.remove(music);
  };

  // Load Playlist from server, convert it to Music instances, then populate self.musics
  self.getPlaylist = function() {
    $.getJSON("/playlist/", function(allData) {
      var mappedMusics = $.map(allData, function(item) {
        return new Music(item);
      });
      self.musics(mappedMusics);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };
}


$(function() {
  musicsPlaylistVM = new PlaylistViewModel();
  musicsLibraryVM = new LibraryViewModel();
  // Local Binding to avoid multi binding by musicsPlaylistVM and musicsLibraryVM
  $('.ko-playlist').each(function(index) {
    ko.applyBindings(musicsPlaylistVM, $('.ko-playlist')[index]);
  });
  $('.ko-library').each(function(index) {
    ko.applyBindings(musicsLibraryVM, $('.ko-library')[index]);
  });

  // TODO Transfer to Redis onSubscribe
  musicsPlaylistVM.getPlaylist();
  musicsLibraryVM.getLibrary();
});


function humanizeSeconds(s) {
  var fm = [
    Math.floor(s / 60) % 60,
    s % 60
  ];
  if(Math.floor(s / 60 / 60) % 24 > 0) {
    fm.unshift(Math.floor(s / 60 / 60) % 24);
  }
  return $.map(fm, function(v) {
    return ((v < 10) ? '0' : '') + v;
  }).join(':');
}


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
        var options = selectPickerOptions.optionsArray,
        optionsText = selectPickerOptions.optionsText,
        optionsValue = selectPickerOptions.optionsValue,
        optionsCaption = selectPickerOptions.optionsCaption,
        isDisabled = selectPickerOptions.disabledCondition || false,
        resetOnDisabled = selectPickerOptions.resetOnDisabled || false;
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
