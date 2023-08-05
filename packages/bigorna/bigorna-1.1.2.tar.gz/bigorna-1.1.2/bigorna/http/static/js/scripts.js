var showOutput = function (url) {
    $.ajax({
        url: url,
        context: document.body
      }).done(function(data) {
          $('#outputContent').text(data);
          $('#outputModal').modal('show');
      }).fail(function() {
          $('.alert').show()
      });
};

var showConfig = function () {
  $('#configModal').modal('show');
};
