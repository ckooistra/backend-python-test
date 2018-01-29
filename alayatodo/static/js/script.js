$(function() {
	$(':checkbox').click(function() {

		var id = $(this).closest('tr').find('td:first').text();
		$.ajax({
			url: '/complete/'+id,
			data: $('form').serialize(),
			type: 'POST',
			success: function(response) {
				console.log(response);
			},
			error: function(error) {
				console.log(error);
			}
		});
	});
});
