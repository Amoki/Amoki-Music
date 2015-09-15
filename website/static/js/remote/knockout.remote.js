// MODEL DEFINITION
// Music model
function Music(data) {
  this.musicId = ko.observable(data.music_id);
  this.name = ko.observable(data.name);
  this.url = ko.observable(data.url);
  this.room = ko.observable(data.room);
  this.date = ko.observable(data.date);
  this.duration = ko.observable(data.duration);
  this.thumbnail = ko.observable(data.thumbnail);
  this.count = ko.observable(data.count);
  this.lastPlay = ko.observable(data.last_play);
  this.deadLink = ko.observable(data.dead_link);
  this.timerStart = ko.observable(data.timer_start);
  this.timerEnd = ko.observable(data.timer_end);
  this.source = ko.observable(data.source);
}
// Room model
function Room(data) {
  this.name = ko.observable(data.name);
  this.timeLeft = ko.observable(data.time_left);
  this.currentTimeLeft = ko.observable(data.current_time_left);
  this.canAdjustVolume = ko.observable(data.can_adjust_volume);
  this.shuffle = ko.observable(data.shuffle);
  this.countLeft = ko.observable(data.count_left);

  // ??
  this.currentMusic = ko.observableArray(new Music(data.current_music));
  // ??

  this.playlist = ko.observableArray([]);
  var mappedMusics = $.map(data.playlist, function(item) {
    return new Music(item);
  });
  this.playlist(mappedMusics);
}
// Source model
function Source(data) {
  this.name = ko.observable(data.name);
}

// VIEW MODEL DEFINITION
// Library view model
function LibraryViewModel() {
  var self = this;

  // library part
  self.musicsLibrary = ko.observableArray([]);
  self.hasPrevious = ko.observable();
  self.hasNext = ko.observable();
  self.currentPage = ko.observable();

  // search part
  self.musicSearch = ko.observableArray([]);
  self.sourceSearch = ko.observable();
  self.querySearch = ko.observable();

  // TEST ONLY
  self.sources = ko.observableArray([
      new Source({name: "Soundcloud test"}),
      new Source({name: "Youtube test"}),
    ]);

  self.addMusic = function() {
    // Return a json serialized Music object
    // $.ajax("/music/", {
    //   data: ko.toJSON({music: this}),
    //   type: "post",
    //   contentType: "application/json",
    //   dataType: "json",
    //   success: function(result) {
    //     newMusic = new Music(result);
    //     roomVM.musics.push(newMusic);
    //     musicsLibraryVM.musicsLibrary.push(newMusic);
    //   }
    // });
    console.log(self.musicsLibrary.indexOf(this));
    console.log(ko.toJSON(this));
  };

  self.searchMusic = function() {
    // Return a json serialized Music object
    if($.type(ko.toJS(self.querySearch)) === "undefined" || !ko.toJS(self.querySearch).trim()) {
      // TODO Display empty field warning
      return;
    }
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

// Room view model
function RoomViewModel() {
  var self = this;

  self.room = ko.observableArray([]);
  self.musicsPlaylist = ko.observableArray([]);

  // Load Playlist from server, convert it to Music instances, then populate self.musicsPlaylist
  // TEMP FUNCTION UNTIL ENDPOINTS ARE USABLE
  self.getPlaylist = function() {
    $.getJSON("/musics/", function(allData) {
      var mappedMusics = $.map(allData, function(item) {
        return new Music(item);
      });
      self.musicsPlaylist(mappedMusics);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  self.getRoom = function() {
    $.getJSON("/room/", function(allData) {
      var room = new Room(allData);
      self.room(room);
    }).fail(function(jqxhr) {
      console.error(jqxhr.responseText);
    });
  };

  self.patchShuffle = function() {
    self.room.shuffle = !self.room.shuffle;
    $.ajax({
      url: '/room/',
      data: ko.toJSON({shuffle: self.room.shuffle}),
      type: 'patch',
      contentType: 'application/json',
      dataType: 'json',
      success: function() {},
      error: logErrors,
    });
  };

  self.postNext = function() {
    $.ajax("/room/next/", {
      data: ko.toJSON({tasks: self.tasks}),
      type: "post",
      contentType: "application/json",
      dataType: 'json',
      success: function() {},
      error: logErrors,
    });
  };
}


$(function() {
  roomVM = new RoomViewModel();
  musicsLibraryVM = new LibraryViewModel();
  // Local Binding to avoid multi binding by roomVM and musicsLibraryVM
  $('.ko-room').each(function(index) {
    ko.applyBindings(roomVM, $('.ko-room')[index]);
  });
  $('.ko-library').each(function(index) {
    ko.applyBindings(musicsLibraryVM, $('.ko-library')[index]);
  });

  // TODO Transfer to Redis onSubscribe
  roomVM.getPlaylist();
  musicsLibraryVM.getLibrary();
});

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

ko.bindingHandlers.stopBinding = {
  init: function() {
    return {controlsDescendantBindings: true};
  }
};
