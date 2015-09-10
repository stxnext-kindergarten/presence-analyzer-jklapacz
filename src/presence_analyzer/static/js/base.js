function parseInterval(value) {
    var result = new Date(1,1,1);
    result.setMilliseconds(value*1000);
    return result;
}

(function($) {
    $(document).ready(function(){
        var loading = $('#loading');
        $.getJSON("/api/v1/users", function(result) {
            var dropdown = $("#user_id");
            $.each(result, function(item) {
                dropdown.append($("<option />").val(this.user_id).text(this.name));
            });
            dropdown.show();
            loading.hide();
        });

        $('#user_id').change(function(){
            var selected_user = $("#user_id").val();
            var chart_div = $('#chart_div');
            if(selected_user) {
                loading.show();
                chart_div.hide();

                showChart(selected_user, chart_div, loading);
            }
        });
    });
})(jQuery);