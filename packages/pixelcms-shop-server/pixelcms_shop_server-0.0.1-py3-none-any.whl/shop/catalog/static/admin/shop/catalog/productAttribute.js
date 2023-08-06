(function($) {
  $(document).ready(function() {
    function valueTypeChanged() {
      if ($('#id_value_type').val() === 'options') {
        $('#options-group').show();
      }
      else {
        $('#options-group').hide();
      }
    }
    valueTypeChanged()
    $('#id_value_type').change(function() {
      valueTypeChanged()
    })
  })
})(grp.jQuery)
